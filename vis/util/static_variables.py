import numpy as np

# Transposition between E-CLASS numbering and our numbering four YOU and Expert
# questions.
# their numbering : our numbering
QUESTION_TRANSPOSITION = {
    1: 1,
    2: 12,
    3: 3,
    4: 26,
    5: 10,
    6: 5,
    7: 29,
    9: 21,
    10: 8,
    11: 11,
    12: 23,
    13: 14,
    14: 27,
    15: 15,
    16: 17,
    17: 25,
    18: 18,
    19: 6,
    20: 19,
    21: 22,
    22: 4,
    23: 20,
    24: 7,
    25: 24,
    26: 13,
    27: 2,
    28: 9,
    29: 28,
    30: 16,
    31: 30
}

# Transposition between E-CLASS numbering and our numbering for the MARK
# questions.
# their numbering : our numbering
MARK_TRANSPOSITION = {
    1: 1,
    2: 10,
    3: 2,
    4: 21,
    5: 8,
    6: 4,
    7: 23,
    9: 17,
    10: 6,
    11: 9,
    12: 19,
    13: 11,
    14: 22,
    15: 12,
    16: 14,
    17: 20,
    18: 15,
    19: 5,
    20: 16,
    21: 18,
    22: 3,
    28: 7,
    30: 13
}

# Text for the YOU and EXPERT questions.
QUESTIONS = [
    "When doing an experiment, I try to understand how the experimental setup works.",
    "If I wanted to, I think I could be good at doing research.",
    "When doing a physics experiment, I don’t think much about sources of systematic error.",
    "If I am communicating results from an experiment, my main goal is to create a report with the correct sections and formatting.",
    "Calculating uncertainties usually helps me understand my results better.",
    "Scientific journal articles are helpful for answering my own questions and designing experiments.",
    "I don’t enjoy doing physics experiments.",
    "When doing an experiment, I try to understand the relevant equations.",
    "When I approach a new piece of lab equipment, I feel confident I can learn how to use it well enough for my purposes.",
    "Whenever I use a new measurement tool, I try to understand its performance limitations.",
    "Computers are helpful for plotting and analyzing data.",
    "I don’t need to understand how the measurement tools and sensors work in order to carry out an experiment.",
    "If I try hard enough I can succeed at doing physics experiments.",
    "When doing an experiment I usually think up my own questions to investigate.",
    "Designing and building things is an important part of doing physics experiments.",
    "The primary purpose of doing a physics experiment is to confirm previously known results.",
    "When I encounter difficulties in the lab, my first step is to ask an expert, like the instructor.",
    "Communicating scientific results to peers is a valuable part of doing physics experiments.",
    "Working in a group is an important part of doing physics experiments.",
    "I enjoy building things and working with my hands.",
    "I am usually able to complete an experiment without understanding the equations and physics ideas that describe the system I am investigating.",
    "If I am communicating results from an experiment, my main goal is to make conclusions based on my data using scientific reasoning.",
    "When I am doing an experiment, I try to make predictions to see if my results are reasonable.",
    "Nearly all students are capable of doing a physics experiment if they work at it.",
    "A common approach for fixing a problem with an experiment is to randomly change things until the problem goes away.",
    "It is helpful to understand the assumptions that go into making predictions.",
    "When doing an experiment, I just follow the instructions without thinking about their purpose.",
    "I do not expect doing an experiment to help my understanding of physics.",
    "If I don’t have clear directions for analyzing data, I am not sure how to choose an appropriate analysis method.",
    "Physics experiments contribute to the growth of scientific knowledge."
]
QUESTIONS = np.array(QUESTIONS)

# Text for the MARK questions.
QUESTIONS_MARK = [
    "... understanding how the experimental setup works?",
    "... thinking about sources of systematic error?",
    "... communicating results with the correct sections and formatting?",
    "... calculating uncertainties to better understand my results?",
    "... reading scientific journal articles?",
    "... understanding the relevant equations?",
    "... learning to use a new piece of laboratory equipment?",
    "... understanding the performance limitations of the measurement tools?",
    "... using a computer for plotting and analyzing data?",
    "... understanding how the measurement tools and sensors work?",
    "... thinking up my own questions to investigate?",
    "... designing and building things?",
    "... confirming previously known results?",
    "... overcoming difficulties without the instructor’s help?",
    "... communicating scientific results to peers?",
    "... working in a group?",
    "... understanding the equations and physics ideas that describe the system I am investigating?",
    "... making conclusions based on data using scientific reasoning?",
    "... making predictions to see if my results are reasonable?",
    "... randomly changing things to fix a problem with the experiment?",
    "... understanding the approximations and simplifications that are included in theoretical predictions?",
    "... thinking about the purpose of the instructions in the lab guide?",
    "... choosing an appropriate method for analyzing data (without explicit direction)?",
]
QUESTIONS_MARK = np.array(QUESTIONS_MARK)
