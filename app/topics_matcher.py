import math
import random
import json
from student import Student
from topic import Topic

class TopicsMatcher:
    def __init__(self,student_ids,topic_ids,student_priorities_map,
                topic_priorities_map,max_accepted_proposals):
        '''
        max_accepted_proposals - Number of topics a student must be assigned.
        Each student accepts no more than max_accepted_proposals proposals as per preferences and 
        rejects the others.
       '''
        self.student_ids = student_ids
        self.topic_ids = topic_ids
        self.max_accepted_proposals = max_accepted_proposals
        self.num_students = len(self.student_ids)
        self.num_topics = len(self.topic_ids)
        if(self.num_topics==0):
            self.num_topics=1        
        #Floor of average number of students assigned each topic.
        self.p_floor = math.floor(self.num_students * max_accepted_proposals/self.num_topics)
        #Ceil of average number of students assigned each topic.        
        self.p_ceil = math.ceil(self.num_students * max_accepted_proposals/self.num_topics)
        print('floor: ',self.p_floor)
        print('ceil: ',self.p_ceil)

        self.students = list(map(lambda student_id: Student(self,student_id,
                        student_priorities_map[student_id]), student_ids))
        self.topics = list(map(lambda topic_id: Topic(self,topic_id,
                        topic_priorities_map[topic_id]), topic_ids))

    def get_student(self,student_id):
        student_id_index = self.student_ids.index(student_id)
        return self.students[student_id_index]

    def get_topic(self,topic_id):
        topic_id_index = self.topic_ids.index(topic_id)
        return self.topics[topic_id_index]

    def is_topics_done_proposing(self):
        is_algorithm_complete = True
        for topic in self.topics:
            if(topic.is_slots_remaining()):
                if not topic.is_proposing_complete():
                    is_algorithm_complete = False
                    break
        return is_algorithm_complete

    def get_student_topic_matches(self):
        matches = dict()
        round = 1

        # Round 1: Topics make their proposals to Students and Students accept proposals upto the limit of topics
        # they can accept.
        print('Round: ',round)
        for topic in self.topics:
            topic.propose(self.p_ceil)

        for student in self.students:
            student.accept_proposal()

        #   The Algorithm repeats for more rounds.
        #   It stops when every topic that has not reached the
        #   maximum quota p_ceil has proposed acceptance to every student.
        if(self.is_topics_done_proposing() == False):
            for _ in iter(int,1):
                round += 1
                print('Round: ',round)
                for topic in self.topics:   
                    topic.propose(topic_remaining_slots = topic.num_remaining_slots)
                for student in self.students:
                    student.accept_proposal()
                if(self.is_topics_done_proposing() == True):
                    print('Topic is done proposing')
                    round = 1
                    break

        for student in self.students:
            matches[student.id] = student.accepted_proposals
        return matches
