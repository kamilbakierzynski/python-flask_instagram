import csv
import time

def append_to_keep_following(people_to_keep_follow):
    with open('data/keep_following.csv', mode='a') as csv_file:
        for row in people_to_keep_follow:
            row += '\n'
            csv_file.write(row)
    csv_file.close()

def overwrite_keep_following(people_to_keep_follow):
    with open('data/keep_following.csv', mode='w') as csv_file:
        for row in people_to_keep_follow:
            row += '\n'
            csv_file.write(row)
    csv_file.close()

def read_keep_following_list():
    follows_to_keep = []
    try:
        with open('data/keep_following.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=' ')
            for row in csv_reader:
                follows_to_keep.append(row[0])
        csv_file.close()
    except:
        pass
    return follows_to_keep


def write_to_last_run(run_list):
    with open('data/last_run.csv', mode='w') as csv_file:
        for row in run_list:
            row += '\n'
            csv_file.write(row)
    csv_file.close()


def read_last_run():
    follows_to_unfollow_from_last_run = []
    try:
        with open('data/last_run.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=' ')
            for row in csv_reader:
                follows_to_unfollow_from_last_run.append(row[0])
        csv_file.close()
    except:
        pass
    return follows_to_unfollow_from_last_run


def append_to_statistics(num_followers, num_follows):
    with open('data/statistics.csv', mode='a') as csv_file:
        row = f'{int(time.time())},{num_followers},{num_follows}'
        row = '\n' + row
        csv_file.write(row)
    csv_file.close()


def display_stats():
    labels = []
    values_followers = []
    values_follows = []
    
    with open('data/statistics.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count != 0:
                if len(row) == 3:
                    labels.append(row[0])
                    values_followers.append(row[1])
                    values_follows.append(row[2])
            line_count += 1
    
    csv_file.close()
    
    return labels, values_followers, values_follows