from transformers import pipeline

summarizer = pipeline("summarization", model="Falconsai/text_summarization")

ARTICLE = """ 
    Recruitment Extensive REPORT
    Candidate		        Lee Jian Yuan
    Overall Score	        6/10
    Leadership		        7/10
    Agility			        6/10
    Cultural Fit		    5/10
    Assessed on		        13 March 2024
    Report generated on	    13 March 2024

    Quickview
                    
    Leadership
    Business Acumen				        8/10
    Dealing with Ambiguity			    5/10
    Strategic thinking				    8/10
    People management and development	6/10
                    
    Agility
    Learning Agility				    7/10
    Cognitive Ability				    5/10
                    
    Cultural Fit
    Purpose Driven				        3/10
    Performance Oriented			    5/10
    Principles Led				        7/10

    Most motivated by: Structuring, Hierarchy, Integrity
    Least motivated by: Security, Absence Of Stress, Cooperativeness
                    
    Work Styles: Positivity, Flexibility, Conceptual
                    
    Leadership
    Leadership is core to organisational success. The section below describes how well does a person's behavioural tendencies, abilities and drivers match the organisation’s leadership framework.

    Business Acumen
    Definition: Demonstrates business savvy and focuses on activities that bring business growth.
    About the Candidate: Lee may be seen as having broad and varied ideas and intellectual interests. Progressive and forward thinking. Focused on innovation and creativity, but being unrealistic or impractical at times. Enjoying working with theoretical or abstract issues and ideas. More interested in focusing on long term strategy and direction. Overly abstract or even pretentious at times.
    Implications: Lee has a tendency to be reliant on business skills and knowledge at the expense of people skills to optimise the business impact of activities. Eager to grasp opportunities to drive business growth, Lee is likely to consistently seek commercial opportunities and conduct activities to grow the business but may overlook the practicality against existing priorities and constraints within the business.

    Dealing with Ambiguity
    Definition: Is able to progress and find a way forward in ambiguous situations.
    About the Candidate: Lee may be seen as having broad and varied ideas and intellectual interests. Progressive and forward thinking. Focused on innovation and creativity, but being unrealistic or impractical at times. Enjoying working with theoretical or abstract issues and ideas. More interested in focusing on long term strategy and direction. Overly abstract or even pretentious at times. Lee may be seen as usually striking a balance between detail focus and big picture perspective. Able to adopt a methodical and planful approach to tasks when necessary. Preferring to be organized, but tending to be less so during stressful periods. Willing to break rules when surrounded by others who are doing so. Developing structured plans, but not always sticking to them. Occasionally missing some critical details in their work. Lee may be seen as confident in sharing opinions they feel strongly about. Enjoying competition and debate as long as it does not get confrontational. Open to changing opinions or decisions if strongly challenged. Sometimes reluctant to challenge others' opinions or express disagreement, but generally willing to do so when necessary. Somewhat uncomfortable advocating for unpopular opinions or decisions. While Lee may at times find it motivating to work in a dynamic environment where the situation is unclear, Lee may also prefer to have certain degree of stability to be able to find a way forward effectively.
    Implications: Implication texts are shown only when you have a high or low score on the competency, as that would suggest a more definitive pattern of behaviour. At the middle range, implications are subjected to situational differences.

    Strategic thinking
    Definition: Assimilates complex information and thinks broadly, considering the wider consequences of plans.
    About the Candidate: Lee may be seen as usually striking a balance between detail focus and big picture perspective. Able to adopt a methodical and planful approach to tasks when necessary. Preferring to be organized, but tending to be less so during stressful periods. Willing to break rules when surrounded by others who are doing so. Developing structured plans, but not always sticking to them. Occasionally missing some critical details in their work. Lee may be seen as having broad and varied ideas and intellectual interests. Progressive and forward thinking. Focused on innovation and creativity, but being unrealistic or impractical at times. Enjoying working with theoretical or abstract issues and ideas. More interested in focusing on long term strategy and direction. Overly abstract or even pretentious at times.
    Implications: Lee may become too absorbed with a situation/problem at a broad conceptual level without translating them into practical solutions and implementation. Often thinking few steps ahead, Lee may overemphasise or overcomplicate plans/situation (e.g. anticipating and planning for several different scenarios or potential hindrances) at the expense of immediate priorities. Lee may face dificulties gaining common understanding with people of a more tactical mindset whom may not see the big picture easily, thus Lee may lack patience to deal with people who do not share the same perspective, and may leave them behind in discussions.

    People management and development
    Definition: Manages and develops individuals to perform at their best.
    About the Candidate: Lee may be willing to take on leadership roles, but also comfortable as a team player. Comfortable leading by example or through direct authority. Able to be directive and controlling when necessary. Prefers to lead a smaller team as opposed to a larger one. Not strongly motivated by accumulating authority and influence. Open to letting others lead in difficult situations or when tough decisions need to be made. Lee may be seen as generally kind and forgiving towards people they know well. Aware of the emotional side of situations, but not overly influenced by it. Sometimes unsympathetic to misfortunes perceived to be caused by poor decisions. Tolerant of others' differences and flaws, but less so under stress. Willing to give difficult feedback even when somewhat uncomfortable. Lee believes that it is important for people in the organisation to be treated fairly. Hence, Lee is likely to delegate tasks in an equal/justifiable manner whilst paying attention to their individual needs to further develop them.
    Implications: Implication texts are shown only when you have a high or low score on the competency, as that would suggest a more definitive pattern of behaviour. At the middle range, implications are subjected to situational differences.

    Agility
    Agility consists of two major components - Learning Agility and Cognitive Ability. Learning Agility is the natural tendency and willingness to learn new information. Cognitive Ability is the ability and 􀂧uidity to learn new information and solve problems in short amount of time.

    Learning Agility
    About You: Lee may be seen as preferring to leverage existing strengths, but willing to develop new ones as well. Believing that people's abilities are dificult to change, but some skills can be developed through hard work, training and education. Interested in helping talented individuals learn and develop. More interested in personal development when there is potential for reward. Reluctant to take on challenging opportunities where there is a high risk of failure. 

    Cognitive Ability
    About You: Lee is somewhat able to process new and complex information accurately, possessing an average speed of learning and problem solving, compared to others.

    Scores Breakdown: Cognitive Ability
    Inductive-Logical Reasoning (5/10)
    About You: Lee is able to analyse and recognise specific trends, patterns or information to generate a general conclusion from it, but may need more time as the complexity increases.
                    
    Numerical Reasoning (3/10)
    About You: Lee may require more time to process new and complex numerical information accurately, as well as retrieving and identifying relevant information to draw logical conclusions.
                    
    Verbal Reasoning (7/10)
    About You: Lee is highly eficient in processing new and complex verbal information accurately, retrieving and identifying relevant information to draw logical conclusions.

    Cultural Fit
    An alignment of employees' preferences, interests and motives with the organisation's value system is an integral part in ensuring both employee satisfaction and business productivity. 

    Purpose Driven
    Definition: Internal motivation to find meaning in the work while strongly identifying to the organisation's mission to achieve ambitious goals.
    Highly driven in finding meaning in work, while identifying with the organisation's overall mission and vision. Does what is necessary to meet targets and achieve what is expected while completing tasks at own pace. Tends to lose energy and commitment to achieve quality results.

    Performance Oriented
    Definition: Sets challenging targets and drives performance to achieve high quality results.
    Role models setting high targets and taking on challenges to achieve more with a sense of urgency to obtain results in the most efficient way. Excels in demonstrating energy and commitment to achieve high quality results. Prefers to finish a task with less regard on the moral side of things, feels that ethics and morales are irrelevant at work.

    Principles Led
    Definition: Holds self-responsible for upholding integrity and the values of the organisation.
    Always strives to ensure work delivered is moral and works with a clear conscience. 

    CBI Guide
    Competency-based Interview (CBI) is an interviewing method where questions are systematically designed and asked to target specific competencies. Conventional, unstructured interviews can be fairly random, and candidate’s responses are often subjected to the perception of an interviewer. Judgement is often formed by general impression given by the candidate, which is highly vulnerable to interviewers’ preconceived notions and biases. In CBI, candidates are queried to provide concrete examples to the questions being asked. The interviewers will follow-up by probing into the examples provided by the candidate to gather evidence about his/her competencies.
    This guide is built based on a competency framework. The candidate's typical or preferred behaviours in relation to the competency framework are displayed on the following pages, followed by suggested questions or areas to probe.  
                    
    Business Acumen
    Suggested Questions
    1.	Share what efforts you have taken in the past to understand your organisation and its business goals and strategies.
        What efforts did you take to understand your business?
        What were your key learnings?
        How did that impact your understanding/perception of your organisation?
        How did you apply your learnings in the future?

    2.	Talk about an important business decision that you have made in the past.
        What factors was driving you to make the decisions?
        How did you implement your decisions?
        What implications did your decision bring to the business?

    Dealing with Ambiguity
    Suggested Questions
    1.	Describe a situation where you had to make an important decision with limited amount of information.
        What did you do prior to making the decision?
        How did you justify and defend your decision?
        What impact did your decision have in the end?

    2.	Talk about an experience where you were required to execute a task without clear structure, information or processes.
        What were your action steps?
        How did you manage the situation?
        What was the end results?

    Strategic thinking
    Suggested Questions
    1.	Share about a situation where you devised a way forward or strategy for a project/your team/organisation.
        What were the factors that you considered?
        How did you implemented the strategy?
        What positive and negative impact did your strategy have?

    2.	Talk about a recent experience where you participated in an important strategic discussion with your team/management.
        What was your role in that discussion?
        What was the ideas/suggestions/thoughts that you contributed?
        How changes/benefits did your contribution bring?

    People management and development
    Suggested Questions
    1.	Give me an example of a time when you contributed to the development of others.
        What was your role in his/her development journey?
        What approach did you use to support his/her development needs?
        How was the person different from before as a result of your involvement?

    2.	Tell me about a time in which you needed to delegate tasks to others.
        How did you decide what tasks to delegate, and to whom?
        What measures did you have in place to monitor performance and hold individuals accountable?
        What was the outcome?
"""

print(summarizer(ARTICLE, max_length=1000, min_length=30, do_sample=False))
# [{'summary_text': 'Hugging Face has emerged as a prominent and innovative force in NLP . From its inception to its role in democratizing AI, the company has left an indelible mark on the industry . The name "Hugging Face" was chosen to reflect the company\'s mission of making AI models more accessible and friendly to humans .'}]