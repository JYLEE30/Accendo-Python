# Import required libraries packages
import logging
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
import sys
import google.api_core.exceptions
import google.generativeai as genai
import time
import re
import json
import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set the logging level
    format='%(asctime)s - %(levelname)s - %(message)s',  # Define log message format
    filename='tp-report-summary.log',  # Specify the log file
    filemode='a'  # Append mode
)

# Create a logger object
logger = logging.getLogger(__name__)

# Read API key from config file
API_KEY = None

try:
    with open('config.json', 'r') as file:
        api_data = json.load(file)
        API_KEY = api_data.get('API_KEY')
    if not API_KEY:
        logger.error("API_KEY not found in api_key.json. Exiting program.")
        sys.exit(0)
except FileNotFoundError:
    logger.error("JSON file not found. Exiting program.")
    sys.exit(0)
except json.JSONDecodeError as e:
    logger.error(f"Error decoding JSON from api key file: {e}. Exiting program.")
    sys.exit(0)
    
# Call function to test AWS Credential
# Check if the bucket is empty or inaccessible
def check_bucket(response):
    try:
        if 'Contents' in response:
            files = [file['Key'] for file in response['Contents'] if not file['Key'].endswith('/') and file['Size'] > 0]

            if files:
                return True  # Bucket has valid files
            else:
                return False  # Bucket is empty or contains only the prefix path
        else:
            return False # Return False to indicate bucket is empty

    except (NoCredentialsError, ClientError) as e:
        logger.error(f"Error: {e}\n")
        return False

# Summarize the given JSON context using gemini model with a customized prompt
def generate_summary(json_input, prompt, retries=3, delay=5):
    # Set up Generative AI API
    for attempt in range(retries):
        try:
            # Set up Generative AI API
            genai.configure(api_key=API_KEY)
            model = genai.GenerativeModel('gemini-1.5-flash-latest')
            full_prompt = f"Full document context:\n\n{json_input}\n\n{prompt}"
            response = model.generate_content(full_prompt)
            return response.text
        except (google.api_core.exceptions.DeadlineExceeded, google.api_core.exceptions.InternalServerError) as e:
            logger.error(f"Attempt {attempt + 1} to generate summary failed with error: {e}")
            if attempt < retries - 1:
                time.sleep(delay)  # Wait before retrying
            else:
                raise

# Replace leading asterisks and hashes with dashes or remove them
def clean_GenAI_format(generated_summary):
    cleaned_context1 = re.sub(r'\#\#\# (.*)', r'\1', generated_summary)  # Remove '###'
    cleaned_context2 = re.sub(r'\#\# (.*)', r'\1', cleaned_context1)  # Remove '##'
    cleaned_context3 = re.sub(r'\* \**', '', cleaned_context2)  # Remove '* **'
    cleaned_context4 = re.sub(r'\*\*', '', cleaned_context3)  # Remove '**'
    cleaned_context5 = re.sub(r'\**', '', cleaned_context4)  # Remove '**'
    cleaned_context6 = re.sub(r'\* ', '', cleaned_context5)  # Remove '* '
    cleaned_context7 = re.sub(r'\*', '', cleaned_context6)  # Remove '*'
    cleaned_context8 = re.sub(r':\**', ': ', cleaned_context7)
    cleaned_context = re.sub(r':\*', ': ', cleaned_context8)
    return cleaned_context

# Split context in response into ExecRep, In-App, and Email
def split_response(cleaned_context):
    parts = cleaned_context.split("In-App", 1)
    if len(parts) < 2:
        raise ValueError("Report text doesn't contain 'In-App' section.")

    # Split second part into email context and subject
    InApp_part, Remaining_part = parts[1], parts[0]
    Email_part = InApp_part.split("Subject:", 1)
    if len(Email_part) < 2:
        raise ValueError("Report text doesn't contain 'Subject:'.")

    return {
        "ExecRep Context": Remaining_part.strip(),  # ExecRep Context is before "In-App"
        "InApp Context": Email_part[0].strip(),  # InApp Context is from "In-App" to before "Subject:"
        "Email Context": "Subject: " + Email_part[1].strip()  # Email Context starts with "Subject:"
    }

# Summarize the given text chunk using gemini model with a specific prompt and full context
def generate_json(separated_context, retries=3, delay=5): 
    # Set up Generative AI API
    for attempt in range(retries):
        try:
            # Set up Generative AI API
            genai.configure(api_key=API_KEY)
            model = genai.GenerativeModel('gemini-1.5-flash-latest')
            full_prompt = f"Change the following text into a usable json format:\n\n{separated_context}"
            context_json = model.generate_content(full_prompt)
            return context_json.text
        except (google.api_core.exceptions.DeadlineExceeded, google.api_core.exceptions.InternalServerError) as e:
            logger.error(f"Attempt {attempt + 1} to generate JSON failed with error: {e}")
            if attempt < retries - 1:
                time.sleep(delay)  # Wait before retrying
            else:
                raise

# Clear JSON GenAI format and parse multiple JSON objects
def clean_and_parse_json(json_Gen):
    # Clean the JSON string by removing leading/trailing characters and newlines
    cleaned_json_head = json_Gen.strip('```json')
    cleaned_json_tail = cleaned_json_head.replace('```', '').strip()
    cleaned_json = cleaned_json_tail.replace('\n', '')
    # Split the cleaned JSON string into individual JSON objects if necessary
    json_objects = cleaned_json.split('\n')

    parsed_json_objects = []
    for json_str in json_objects:
        try:
            parsed_json = json.loads(json_str)
            parsed_json_objects.append(parsed_json)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON format: {e}")
            continue

    return parsed_json_objects

# Copy processed file to another S3 folder
def copy_file(s3, source_bucket, source_key, destination_bucket, destination_key):
    try:
        s3.copy_object(
            Bucket=destination_bucket,
            CopySource={'Bucket': source_bucket, 'Key': source_key},
            Key=destination_key
        )
        logger.info(f"Copied {source_key} to {destination_key}")
    except Exception as e:
        logger.error(f"Failed to copy {source_key} to {destination_key}: {e}")

# Delete the original file from S3
def delete_file(s3, bucket, key):
    try:
        s3.delete_object(Bucket=bucket, Key=key)
        logger.info(f"Deleted {key} from {bucket}\n")
    except Exception as e:
        logger.error(f"Failed to delete {key} from {bucket}: {e}\n")

# Structure and upload JSON
def structure_and_upload_json(s3, OUTPUT_BUCKET, output_key, parsed_json):
    # Save the response as a JSON file
    try:
        s3.put_object(Bucket=OUTPUT_BUCKET, Key=output_key, Body=json.dumps(parsed_json, ensure_ascii=False, indent=4))
        logger.info(f"Uploaded JSON to S3: s3://{OUTPUT_BUCKET}/{output_key}")
    except Exception as e:
        logger.error(f"Failed to upload JSON to S3: {e}")

# Main function to select, run, and process JSON file
def main():
    # Create an S3 client object for the specified AWS region
    s3 = boto3.client('s3', region_name='ap-southeast-1')

    # Specify the bucket name and prefix to read files from
    INPUT_BUCKET = 'tp-report-summary'
    INPUT_PREFIX = 'tp-dev/to_process/'
    OUTPUT_BUCKET = 'tp-report-summary'
    FAILED_PREFIX = 'tp-dev/processed_files/Failed/'
    SUCCEED_PREFIX = 'tp-dev/processed_files/Successful/'
    JSON_EXECREP_PREFIX = 'tp-dev/output/JSON_ExecutiveReport/'
    JSON_INAPP_PREFIX = 'tp-dev/output/JSON_InApp/'
    JSON_EMAIL_PREFIX = 'tp-dev/output/JSON_Email/'

    # List objects in the S3 bucket with the specified prefix
    response = s3.list_objects_v2(Bucket=INPUT_BUCKET, Prefix=INPUT_PREFIX)
    
    # Call function to test AWS Credential
    # Check if the bucket is empty or inaccessible
    if check_bucket(response):
        logger.info("Files found in bucket. Proceeding with processing.")
    else:
        logger.info("No files found in bucket. Exiting program.")
        sys.exit()

    # Filter out directories or 'folders' from the list of files
    files = [file['Key'] for file in response['Contents'] if not file['Key'].endswith('/')]
    
    # Sort the files by their LastModified timestamp in ascending order
    files = sorted(files, key=lambda x: response['Contents'][files.index(x)]['LastModified'])

    # Define specific prompts for each text (customize as needed)
    prompt = """
        (1) Retrieve the following information:
            - Report Type, Project Name, Project Level
            - Candidate ID, Email, Name, Overall Average
            - All competencies and their sten (exclude Cognitive Tools Percentile)
            - All sub-competencies under the 3 main competencies and their sten
            - Top 3 motivators, bottom 3 demotivators
            - Top 3 work-related behaviors
        (2) For each sub-competency in main competency 1 section,
            - summarize comments (score description, implications, development tips) in 18 words
            - retrieve and summarize one key question from CBI questions in 10 words, excluding sub-questions
            - replace all (Name) with Cand
        (3) For each sub-competency in main competency 2 section,
            - summarize comments in 18 words
            - for each breakdown in sub-competency 2, retrieve sten and summarize score description in 18 words
            - replace all (Name) with Cand
        (4) For each sub-competency in main ompetency 3 section,
            - summarize category description in 18 words for low if sten less than or equal to 5
            - summarize category description in 18 words for high if sten greater than or equal to 6
            - replace all (Name) with Cand
        (5) Analyze the full JSON context to suggest 3 possible derailers with brief descriptions in 18 words
        (6) Summarize each response in (2) and (4) into a single paragraph with essential details in 24 words
            - Focus on explaining the candidate's strength and weakness based on each of their sub-competencies in (2), (4) and (5)
            - Use the same response in (1), just exclude the sub-competencies
            - Use the exact same response in (3) and (5)
            - replacing all (Name) with Cand
        (7) Summarize the response into a shorter email format with essential details, replace all (Name) with Cand

        Format (1) output as below: (Don't add section header on your own)
        Report Type: {Report Type}
        Project Name: {Project Name}
        Project Level: {Project Level}

        Candidate Name: {Candidate Name}
        Candidate ID: {Candidate ID}
        Candidate Email: {Candidate Email}
                
        Overall Average: {Overall Average}
        {Main Competency 1's name}: {Main Competency 1's sten}
            + {Main Competency 1's sub-competecy 1's name}: {Main Competency 1's sub-competecy 1's sten}
            Continue to add remaining sub-competecies of main competency 1.
        {Main Competency 2's name}: {Main Competency 2's sten}
            + {Main Competency 2's sub-competecy 1's name}: {Main Competency 2's sub-competecy 1's sten}
            + {Main Competency 2's sub-competecy 2's name}: {Main Competency 2's sub-competecy 2's sten}
        End here for main competency 2, exclude breakdown in cognitive ability
        {Main Competency 3's name}: {Main Competency 3's sten}
            + {Main Competency 3's sub-competecy 1's name}: {Main Competency 3's sub-competecy 1's sten}
        Ignore the None of main competency 3's sten and continue to add remaining sub-competecies of main competency 3.
        
        Motivators: {motivator 1, motivator 2, motivator 3}
        Demotivators: {demotivator 1, demotivator 2, demotivator 3}
        Preferable work styles: {work related behaviour 1, work related behaviour 2, work related behaviour 3}

        Format (2) output as below: (Don't add section header on your own)
        {Main Competency 1's name}
        {Main Competency 1's sub-competecy 1's name}: Summarized paragraph.
        CBI Question: {Most Important Main Question from CBI Question}
        Continue to add remaining sub-competencies in the {Main Competency 1} section and Main Question from CBI Question using the format above.

        Format (3) output as below: (Don't add section header on your own)
        {Main Competency 2's name}
        {Main Competency 2's sub-competecy 1's name}: Summarized comment paragraph.
        {Main Competency 2's sub-competecy 2's name}: Summarized comment paragraph.
            + {Main Competency 2's sub-competecy 2's Breakdown 1's name} ({Sten}): Summarized paragraph of breakdown.
            + {Main Competency 2's sub-competecy 2's Breakdown 2's name} ({Sten}): Summarized paragraph of breakdown.
            + {Main Competency 2's sub-competecy 2's Breakdown 3's anme} ({Sten}): Summarized paragraph of breakdown.

        Format (4) output as below: (Don't add section header on your own)
        {Main Competency 3's name}
        {Main Competency 3's sub-competecy 1's name}: Summarized definition and comment.
        Continue to add remaining sub-competencies in the {Main Competency 3} section using the format above.
        
        Format (5) output as below: (Don't add section header on your own)
        Possible derailers
        1. {Derailer 1 Title}: {Brief Description}
        2. {Derailer 2 Title}: {Brief Description}
        3. {Derailer 3 Title}: {Brief Description}

        Format (6) output as below: (Don't add section header on your own)
        In-App
        Report Type: {Report Type}
        Project Name: {Project Name}
        Project Level: {Project Level}

        Candidate Name: {Candidate Name}
        Candidate ID: {Candidate ID}
        Candidate Email: {Candidate Email}
        
        Overall Average: {Overall Average}
        {Main Competency 1's name}: {Main Competency 1's sten}
        {Main Competency 2's name}: {Main Competency 2's sten}
        {Main Competency 3's name}: {Main Competency 3's sten}

        Key Highlights:
        Strengths: {From your response} in 15 words
        Areas for Development: {From your response} in 15 words
        
        Possible derailers
        1. {Derailer 1 Title}: {Brief Description}
        2. {Derailer 2 Title}: {Brief Description}
        3. {Derailer 3 Title}: {Brief Description}

        Motivators: {motivator 1, motivator 2, motivator 3}
        Demotivators: {demotivator 1, demotivator 2, demotivator 3}
        Preferable work styles: {work related behaviour 1, work related behaviour 2, work related behaviour 3}

        {Main Competency 1's name}
        Summarized paragraph of (2)

        Response in (3)

        {Main Competency 3's name}
        Summarized paragraph of (4)

        Format (7) output as below: (Don't add section header on your own)
        Subject: Recruitment Report for {Candidate Name}

        Dear Hiring Manager,
        this email summarizes the assessment results for candidate {Candidate Name}. 

        Overall score: {Overall Average}
                
        {Main Competency 1's name}: {Main Competency 1's sten}
        {Main Competency 2's name}: {Main Competency 2's sten}
        {Main Competency 3's name}: {Main Competency 3's sten}

        Key Highlights:
        Strengths: {From your response} in 10 words
        Areas for Development: {From your response} in 10 words
        Possible Derailers: {From your response}

        Motivators: {From your response}
        Demotivators: {From your response}
        Preferable Work Styles: {From your response}

        For a detailed analysis of his/her sub skills and other components,
        please review his/her Executive Report or Full Report attached to this email.

        Thank you for using our product.

        Best regards,
        Accendo Technologies
    """

    # Iterate over each file object in the sorted list
    for key in files:       
        # Get the object (file) from S3 using its key
        obj = s3.get_object(Bucket=INPUT_BUCKET, Key=key)
        
        # Read and decode the object's content assuming it's UTF-8 encoded
        json_context = obj['Body'].read().decode('utf-8')
        
        # Log the read file
        logger.info(f"Reading file: {key}...")

        try:
            generated_summary = generate_summary(json_context, prompt, retries=3, delay=5)
        except (google.api_core.exceptions.DeadlineExceeded, google.api_core.exceptions.InternalServerError) as e:
            logger.error(f"Failed to generate summary after retries: {e}")
            # Copy the file to the failed folder
            failed_key = key.replace(INPUT_PREFIX, FAILED_PREFIX)
            try:
                copy_file(s3, INPUT_BUCKET, key, OUTPUT_BUCKET, failed_key)
                # Check if the file exists in the processed folder
                check = s3.head_object(Bucket=OUTPUT_BUCKET, Key=failed_key)

                if check['ResponseMetadata']['HTTPStatusCode'] == 200:
                    # Delete the original file from the input folder
                    delete_file(s3, INPUT_BUCKET, key)
                else:
                    logger.error(f"Failed to verify the file in the processed folder: {failed_key}")
            except Exception as copy_delete_error:
                logger.error(f"Failed to copy and verify the file: {copy_delete_error}")
                continue

        cleaned_context = clean_GenAI_format(generated_summary)
        splitted_context = split_response(cleaned_context)

        # Get splitted context
        ExecRep_Context = splitted_context["ExecRep Context"]
        InApp_Context = splitted_context["InApp Context"]
        Email_Context = splitted_context["Email Context"]

        # Generate JSON
        try:
            json_ExecRep_Gen = generate_json(ExecRep_Context, retries=3, delay=5)
        except (google.api_core.exceptions.DeadlineExceeded, google.api_core.exceptions.InternalServerError) as e:
            logger.error(f"Failed to generate JSON after retries: {e}")
            # Copy the file to the failed folder
            failed_key = key.replace(INPUT_PREFIX, FAILED_PREFIX)
            try:
                copy_file(s3, INPUT_BUCKET, key, OUTPUT_BUCKET, failed_key)
                # Check if the file exists in the processed folder
                check = s3.head_object(Bucket=OUTPUT_BUCKET, Key=failed_key)

                if check['ResponseMetadata']['HTTPStatusCode'] == 200:
                    # Delete the original file from the input folder
                    delete_file(s3, INPUT_BUCKET, key)
                else:
                    logger.error(f"Failed to verify the file in the processed folder: {failed_key}")
            except Exception as copy_delete_error:
                logger.error(f"Failed to copy and verify the file: {copy_delete_error}")
                continue

        try:
            json_InApp_Gen = generate_json(InApp_Context, retries=3, delay=5)
        except (google.api_core.exceptions.DeadlineExceeded, google.api_core.exceptions.InternalServerError) as e:
            logger.error(f"Failed to generate JSON after retries: {e}")
            # Copy the file to the failed folder
            failed_key = key.replace(INPUT_PREFIX, FAILED_PREFIX)
            try:
                copy_file(s3, INPUT_BUCKET, key, OUTPUT_BUCKET, failed_key)
                # Check if the file exists in the processed folder
                check = s3.head_object(Bucket=OUTPUT_BUCKET, Key=failed_key)

                if check['ResponseMetadata']['HTTPStatusCode'] == 200:
                    # Delete the original file from the input folder
                    delete_file(s3, INPUT_BUCKET, key)
                else:
                    logger.error(f"Failed to verify the file in the processed folder: {failed_key}")
            except Exception as copy_delete_error:
                logger.error(f"Failed to copy and verify the file: {copy_delete_error}")
                continue

        try:
            json_Email_Gen = generate_json(Email_Context, retries=3, delay=5)
        except (google.api_core.exceptions.DeadlineExceeded, google.api_core.exceptions.InternalServerError) as e:
            logger.error(f"Failed to generate JSON after retries: {e}")
            # Copy the file to the failed folder
            failed_key = key.replace(INPUT_PREFIX, FAILED_PREFIX)
            try:
                copy_file(s3, INPUT_BUCKET, key, OUTPUT_BUCKET, failed_key)
                # Check if the file exists in the processed folder
                check = s3.head_object(Bucket=OUTPUT_BUCKET, Key=failed_key)

                if check['ResponseMetadata']['HTTPStatusCode'] == 200:
                    # Delete the original file from the input folder
                    delete_file(s3, INPUT_BUCKET, key)
                else:
                    logger.error(f"Failed to verify the file in the processed folder: {failed_key}")
            except Exception as copy_delete_error:
                logger.error(f"Failed to copy and verify the file: {copy_delete_error}")
                continue

        # Cleaned and Parsed as JSON format
        parsed_json_ExecRep = clean_and_parse_json(json_ExecRep_Gen)
        parsed_json_InApp = clean_and_parse_json(json_InApp_Gen)
        parsed_json_Email = clean_and_parse_json(json_Email_Gen)

        # Define each JSON file name
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_key_ExecRep = f"{JSON_EXECREP_PREFIX}{key.split('/')[-1].replace('.json', '_')}ExecRep_{timestamp}.json"
        output_key_InApp = f"{JSON_INAPP_PREFIX}{key.split('/')[-1].replace('.json', '_')}InApp_{timestamp}.json"
        output_key_Email = f"{JSON_EMAIL_PREFIX}{key.split('/')[-1].replace('.json', '_')}Email_{timestamp}.json"
        
        # Structure and Upload JSON
        structure_and_upload_json(s3, OUTPUT_BUCKET, output_key_ExecRep, parsed_json_ExecRep)
        structure_and_upload_json(s3, OUTPUT_BUCKET, output_key_InApp, parsed_json_InApp)
        structure_and_upload_json(s3, OUTPUT_BUCKET, output_key_Email, parsed_json_Email)
        
        # Copy the original file to the processed folder
        succeed_key = key.replace(INPUT_PREFIX, SUCCEED_PREFIX)
        try:
            copy_file(s3, INPUT_BUCKET, key, OUTPUT_BUCKET, succeed_key)
            check = s3.head_object(Bucket=OUTPUT_BUCKET, Key=succeed_key)
            if check['ResponseMetadata']['HTTPStatusCode'] == 200:
                # Delete the original file from the input folder
                delete_file(s3, INPUT_BUCKET, key)
            else:
                logger.error(f"Failed to verify the file in the processed folder: {succeed_key}")
        except Exception as copy_delete_error:
            logger.error(f"Failed to copy and verify the file: {copy_delete_error}")
            continue

if __name__ == "__main__":
    main()