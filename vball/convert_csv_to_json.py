# this imports all the libraries we need
import sys
import os
import csv
import json


def convert_csv_to_json(match_id, csv_data):

    team_a_games_won = csv_data[3][21]
    team_b_games_won = csv_data[4][21]

    if int(team_a_games_won) > int(team_b_games_won):
        victor = 'team_a'
    else:
        victor = 'team_b'

    first_serving = None

    if csv_data[27][0].lower() == 'x':
        first_serving = 'right'
        firstservescores = 30
        firstreceivescores = 27
        secondservescores = 61
        secondreceivescores = 58
        
    else:
        first_serving = 'left'
        firstservescores = 27
        firstreceivescores = 30
        secondservescores = 58
        secondreceivescores = 61



    result = {
        'match_id': match_id,
        'team_a': csv_data[2][0],
        'team_b': csv_data[4][0],
        'winner': victor,
        'games': [
            {
                'left': 'team_a',
                'right': 'team_b',
                'left_score': int(csv_data[3][12]),
                'right_score': int(csv_data[4][12]),
                'server': first_serving,
                'left_timeouts': detect_timeouts(35,1,csv_data),
                'right_timeouts': detect_timeouts(35,3,csv_data),
                'scores': scores_in_order(get_sideouts(get_score_array(firstservescores, csv_data), get_score_array(firstreceivescores, csv_data), first_serving))

            },
            {
                'left': 'team_b',
                'right': 'team_a',
                'left_score': int(csv_data[4][15]),
                'right_score': int(csv_data[3][15]),
                'server': first_serving,
                'left_timeouts': detect_timeouts(66,1,csv_data),
                'right_timeouts': detect_timeouts(66,3,csv_data),
                'scores': scores_in_order(get_sideouts(get_score_array(secondservescores, csv_data), get_score_array(secondreceivescores, csv_data), first_serving))
            } 
        ]
    }

    if int(team_a_games_won) == 1 or int(team_b_games_won) == 1:

        thirdservescores = 0
        thirdreceivescores = 0

        if csv_data[89][0] == 'x':
            first_serving = 'right'
            thirdservescores = 92
            thirdreceivescores = 89

        else:
            first_serving = 'middle'
            thirdservescores - 89
            thirdreceivescores = 92


        middle_team = None
        right_team = None

        if csv_data[71][2] == 'A':
            middle_team = 'team_a'
            right_team = 'team_b'
        else:
            middle_team = 'team_b'
            right_team = 'team_a'
        result['games'].append({
            'middle': middle_team,
            'right': right_team,
            'server': first_serving,
            'middle_score': int(csv_data[3][18]),
            'right_score': int(csv_data[4][18]),
            'middle_timeouts': detect_timeouts(97,1,csv_data),
            'right_timeouts': detect_timeouts(97,3,csv_data),
            'scores': scores_in_order(get_sideouts(get_score_array(thirdservescores, csv_data), get_score_array(thirdreceivescores, csv_data), first_serving)) 
        })

    


    return result

def detect_timeouts(x, y, csv_data):
    timeouts = []
    if csv_data[x - 1][y - 1] == "":
        return timeouts

    first_timeout = [
        int(csv_data[x - 1][y - 1]),
        int(csv_data[x - 1][y])
    ]
    timeouts.append(first_timeout)


    if csv_data[x][y] == "":
        return timeouts

    second_timeout = [
        int(csv_data[x][y - 1]),
        int(csv_data[x][y])
    ]
    timeouts.append(second_timeout)
    return timeouts

def get_score_array(x, csv_data):
    
    score_array = []

    for cell in csv_data[x]:
        if cell == '':
            break

        if cell == 'x':
            score_array.append(0)
        else:
            score_array.append(int(cell))
    
    return score_array

def get_sideouts(serve_points, receive_points, side_of_serve):
    
    receive_points[0] = 0
    serve_iter = 0
    receive_iter = 0

    iter_receive = True

    anchor_points = []

    anchor_points.append([0, 0])

    if side_of_serve == 'middle' or side_of_serve == 'left':
       

        for points in range(len(receive_points) + len(serve_points)):
            
            try:

                anchor_points.append([serve_points[serve_iter], receive_points[receive_iter]])

                            
                if iter_receive:
                    receive_iter += 1
                    iter_receive =  not iter_receive
                else:
                    serve_iter += 1
                    iter_receive = not iter_receive
                
            except IndexError:

                # anchor_points.append([serve_points[len(serve_points) - 1], receive_points[len(receive_points) - 1]])
                break

            
    else:


        for points in range(len(receive_points) + len(serve_points)):

            try:
                
                anchor_points.append([receive_points[receive_iter], serve_points[serve_iter]])

                        
                if iter_receive:
                    receive_iter += 1
                    iter_receive =  not iter_receive
                else:
                    serve_iter += 1
                    iter_receive = not iter_receive

            except IndexError:

                # anchor_points.append([receive_points[len(receive_points) - 1], serve_points[len(serve_points) - 1]])
                break

            
    return anchor_points

        

def scores_in_order(anchor_points):

    final_score_array = []
    i = 0

    

    points_total = anchor_points[len(anchor_points) - 1][0] + anchor_points[len(anchor_points) - 1][1]


    # final_score_array.append([anchor_points[i][0], anchor_points[i][1]])

    
    for overall in range(points_total):

        amount = 1
        oamount = 1
        
        try: 
            for diff in range(anchor_points[i][0], anchor_points[i+1][0]):
                
                final_score_array.append([anchor_points[i][0] + amount, anchor_points[i][1]])

                amount += 1

            for odiff in range(anchor_points[i][1], anchor_points[i+1][1]):
                
                final_score_array.append([anchor_points[i][0], anchor_points[i][1] + oamount])
                oamount += 1
            i += 1
        except IndexError:
            break
    
        
    return final_score_array


def read_csv_data(filename):
    csv_data = []
    with open(filename) as f:
        for row in csv.reader(f):
            csv_data.append(row)
    return csv_data


def write_json_data(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2, sort_keys=True)


def main():
    # Make sure they specified a file
    if len(sys.argv) != 2:
        print 'You forgot to specify a filename.'
        exit(1)

    # Get the file name
    csv_filename = sys.argv[1]
    match_id = csv_filename[:36]

    # Make sure the file exists
    if not os.path.isfile(csv_filename):
        print "The file '{}' doesn't exist".format(csv_filename)
        exit(1)

    # Read the data
    csv_data = read_csv_data(csv_filename)
    # Convert the data
    json_data = convert_csv_to_json(match_id, csv_data)

    # Get the new filename
    json_filename = match_id + '.json'
    # Write the json data
    write_json_data(json_filename, json_data)


if __name__ == '__main__':
    main()
