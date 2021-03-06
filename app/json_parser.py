import json
import random
import operator
from collections import Counter
import collections

class JsonParser:
   
    def __init__(self,data):        
        self.input_data_dict = data
        self.topic_ids = self.input_data_dict["tid"]
        self.input_data_dict["users"].keys()
        self.student_ids = list(self.input_data_dict["users"].keys())

        self.topics_counts = Counter
        self.topic_lists = []
        self.calculate_popular_topics()
        self.student_priorities_dict = self.create_student_priorities(self.input_data_dict)
        self.topic_priorities_dict = self.create_topic_priorities(self.input_data_dict)
        self.max_accepted_proposals = int(self.input_data_dict["max_accepted_proposals"])

    def create_student_priorities(self,json_dict):
        student_priorities_dict = dict()
        for student_id in self.student_ids:
            chosen_topic_ids = json_dict["users"][student_id]["tid"]
            popular_tuple = self.topics_counts.most_common(3)
            popular_topics_list = [x[0] for x in popular_tuple]

            # Check if student has topics they"d like to bid
            if not chosen_topic_ids:
                topic_already_chosen = json_dict["users"][student_id]["otid"]
                all_topics = list()
                all_topics = self.topic_ids
                random.shuffle(all_topics)
                # Reduce priority of popular topics 
                for popular_topic in popular_topics_list:               
                    if popular_topic in all_topics:                        
                        all_topics.remove(popular_topic)
                        all_topics.append(popular_topic)                

                if topic_already_chosen in all_topics:
                    # Check if student already choose a topic and remove it from priorities list
                    all_topics.remove(topic_already_chosen)
                all_topics.append(topic_already_chosen)
                student_priorities_dict[student_id] = []
                student_priorities_dict[student_id] += all_topics
                self.input_data_dict["users"][student_id]["priority"] = random.sample(range(1, len(student_priorities_dict[student_id])+1), len(student_priorities_dict[student_id]))
                self.input_data_dict["users"][student_id]["time"] = [0]
            else:
                chosen_topic_priorities = json_dict["users"][student_id]["priority"]
                student_priorities_dict[student_id] = [x for x,_ in
                                                       sorted(zip(chosen_topic_ids,
                                                       chosen_topic_priorities))]
                unchosen_topic_ids = list(set(self.topic_ids).difference(set(
                                     chosen_topic_ids)))
                topic_already_chosen = json_dict["users"][student_id]["otid"]
                if topic_already_chosen in unchosen_topic_ids:
                    unchosen_topic_ids.remove(topic_already_chosen)
                random.shuffle(unchosen_topic_ids)
                             
                for popular_topic in popular_topics_list:                    
                    if popular_topic in unchosen_topic_ids:                        
                        unchosen_topic_ids.remove(popular_topic)
                        unchosen_topic_ids.append(popular_topic) # Add popular topic to end to not assign it

                student_priorities_dict[student_id] += unchosen_topic_ids                 
                student_priorities_dict[student_id].append(topic_already_chosen)
        return student_priorities_dict

    def calculate_popular_topics(self):
        for student_id in self.student_ids:
            chosen_topic_ids = self.input_data_dict["users"][student_id]["tid"]            
            self.topic_lists += chosen_topic_ids                        
            self.topics_counts = Counter(self.topic_lists)              

    def create_topic_priorities(self,json_dict):
        topic_priorities_dict = dict()
        for total_topic_id in self.topic_ids:
            topic_priorities_dict[total_topic_id] = []
            for student_id in self.student_ids:
                # Check if items in total topic list is within student topic list
                if(total_topic_id in self.student_priorities_dict[student_id]):
                    timestamp = max(json_dict["users"][student_id]["time"])
                    topic_priority = self.student_priorities_dict[
                                     student_id].index(total_topic_id)
                    num_chosen_topics = len(json_dict["users"][student_id][
                                        "tid"])
                    topic_priorities_dict[total_topic_id].append((student_id,
                                                    topic_priority,
                                                    num_chosen_topics,
                                                    timestamp))
            topic_priorities_dict[total_topic_id].sort(key = operator.itemgetter(1,2,
                                                 3))
            topic_priorities_dict[total_topic_id] = [x for x,_,_,_ in
                                              topic_priorities_dict[total_topic_id]]
        return topic_priorities_dict
