# Name: Yichun Zhou
# NYU NetID: yz6176
# Homework 3: Election prediction

import csv
import os
import time

def read_csv(path):
    """
    Reads the CSV file at path, and returns a list of rows. Each row is a
    dictionary that maps a column name to a value in that column, as a string.
    """
    output = []
    for row in csv.DictReader(open(path)):
        output.append(row)
    return output

################################################################################
# Problem 1: State edges
################################################################################

def row_to_edge(row):
    """
    Given an election result row or poll data row, returns the Democratic edge
    in that state.
    """
    return float(row["Dem"]) - float(row["Rep"])  

def state_edges(election_result_rows):
    """
    Given a list of election result rows, returns state edges.
    The input list does has no duplicate states;
    that is, each state is represented at most once in the input list.
    """
    #TODO: Implement this function
    #Call a new dict
    state_edges_dict = {}
    #for loop iterate through the data rows
    for row in election_result_rows:
        # set key as the State name
        key = row['State']
        # value = the return from function row_to_edge
        value = row_to_edge(row)
        # store key, value into dict
        state_edges_dict.update({key:value})
    #return the dictionary
    return state_edges_dict
    pass

    #Report: used a dictionary to store State and row_to_edge
    #state as key
    #the caculation result by row_to_edge is the value

################################################################################
# Problem 2: Find the most recent poll row
################################################################################

import time
def earlier_date(date1, date2):
    """
    Given two dates as strings (formatted like "Oct 06 2012"), returns True if 
    date1 is after date2.
    """
    return (time.strptime(date1, "%b %d %Y") < time.strptime(date2, "%b %d %Y"))

#earlier_date("Jan 01 2012", "Jan 02 2012")

def most_recent_poll_row(poll_rows, pollster, state):
    """
    Given a list of poll data rows, returns the most recent row with the
    specified pollster and state. If no such row exists, returns None.
    """
    #TODO: Implement this function
    #initiate a dict with assigned value
    recent_dict = {"ID":0, "State":"WA", "Pollster":"A", "Date":"Jan 01 1989"}
    #for loop read all rows from poll_rows
    for row in poll_rows:
        current_state = row['State']
        current_p = row['Pollster']
        # check the state, pollster, and Date value for this row 
        # if earlier_date function return False, update the Date
        if ((state == current_state) & (pollster == current_p) & 
            (earlier_date(row['Date'], recent_dict['Date']) != True)):
            #update the Date for the specific state and pollster
            # recent_dict.update({"ID":row['ID'], "State":state, 
            #                    "Pollster":pollster,'Date':row['Date']})
            recent_dict.update(row)
    #if there is no condition matched, the date woudl same as the inition value
    if (recent_dict['Date'] == "Jan 01 1989"):
        # recent_dict will return None
        recent_dict = None
    return recent_dict
    pass

    #Report: used a loop to iterate through the poll_rows
    #used 3 condtions in the if to replace for the most recent poll row
    #check with the predifined value, if the same, 
    #means no state and poll matched

################################################################################
# Problem 3: Pollster predictions
################################################################################

def unique_column_values(rows, column_name):
    """
    Given a list of rows and the name of a column (a string), returns a set
    containing all values in that column.
    """
    #TODO: Implement this function
    # a new dictionary
    column_values = {}
    #int i for store dict value
    i = 0
    #for loop to read from rows
    for row in rows:
        #store column_values as key in dict
        column_values.update({row[column_name]:i})
        i += 1
        
    # retunr the key of the dict, get unique value
    return column_values.keys()
    pass

    #Report: dict data structure is very helpful to store unique values
    #for loop to iterate through rows, and store the column_name as dictionary
    #key, becasue key is always a unique value

def pollster_predictions(poll_rows):
    """
    Given a list of poll data rows, returns pollster predictions.
    """
    #a new dict, should be {key:{key:value}} in the end
    pridiction = dict()
    #i = 0
    # call unique function for Pollster
    uni_poll = unique_column_values(poll_rows,'Pollster')
    #print(uni_poll)
    # call unique function for State
    uni_state = unique_column_values(poll_rows,'State')
    #print(uni_state)
    #loop in unique pollster

    for p in uni_poll:
        pridiction[p]={}

    for p in pridiction:
        #print(p)
        for s in uni_state:
            #print(s)
            #call most_recent_poll_row function set pollster as unique pollster
            #set state as the unique state
            most_recent_poll = most_recent_poll_row(poll_rows, p, s)    
            # check if most_recent_poll is none
            if most_recent_poll is not None:
                  # call row_to_edge fcuntion to get edge_score
                edge_score = row_to_edge(most_recent_poll)
                  # update dict with state and edge_score
                pridiction[p].update({most_recent_poll['State']:edge_score})
            # pass if most_recent_poll is none
            else:
                pass
    return pridiction
    pass

    #Report: first loop is used to store p as the keys and give empty values
    #used 2 foor to iterate through the unique pollster and state, 
    #call most_recent_poll_row function to get the most recent poll

################################################################################
# Problem 4: Pollster errors
################################################################################

def average_error(state_edges_predicted, state_edges_actual):
    """
    Given predicted state edges and actual state edges, returns
    the average error of the prediction.
    """
    #TODO: Implement this function
    #initiate 3 int value, set them = 0
    #to store average error later
    ave_err = 0
    #to store number of same state in both passing variable 
    count = 0
    #sum up the totol error
    total_err = 0
    #first loop in state_edges_predicted
    for p in state_edges_predicted:
        #second loop in state_edges_predicted
        for s in state_edges_actual:
            # if value are the same
            if p == s :
                #count + 1
                count += 1
                # total error cacualte use absulute value fucntion
                total_err += abs(state_edges_predicted[p]-state_edges_actual[s])
                #average = total / count
                ave_err = total_err/count
            # no same value
            elif count == 0:
                #set ave_err to None
                ave_err = None
    return ave_err
    pass 

    #Report: used 2 foor to iterate through the two passing varaible
    #compared for same state and caculated average error
    
def pollster_errors(pollster_predictions, state_edges_actual):
    """
    Given pollster predictions and actual state edges, retuns pollster errors.
    """
    #TODO: Implement this function
    # takes two dictionaries and returns the average error by pollster in a dictionary
    # generate a new dict
    poll_error = {}
    #iterate through the prediction dict
    for p in pollster_predictions:
        #call average_error function to find error score for each state
        ave_err = average_error(pollster_predictions[p],state_edges_actual)
        #store into dict
        poll_error.update({p:ave_err})
    return poll_error
    pass

    #Report: used a foor to iterate through the predictions dictionary
    #compared for same state and caculated average error using function defined 
    #in previous and store to a new dict

################################################################################
# Problem 5: Pivot a nested dictionary
################################################################################

def pivot_nested_dict(nested_dict):
    """
    Pivots a nested dictionary, producing a different nested dictionary
    containing the same values.
    The input is a dictionary d1 that maps from keys k1 to dictionaries d2,
    where d2 maps from keys k2 to values v.
    The output is a dictionary d3 that maps from keys k2 to dictionaries d4,
    where d4 maps from keys k1 to values v.
    For example:
      input = { "a" : { "x": 1, "y": 2 },
                "b" : { "x": 3, "z": 4 } }
      output = {'y': {'a': 2},
                'x': {'a': 1, 'b': 3},
                'z': {'b': 4} }
    """
     #TODO: Implement this function
    #generate a new dict
    new_dict = {}
    #interate key though passing variable
    for i in nested_dict:
        # get the new key for output
        new_key = nested_dict[i]
        #interate through new keys to get specific key and assign value
        for j in new_key:
            # check if the key is already in the output
            if j in new_dict :
                #if yes, add on to the dict
                new_dict[j].update({i:new_key[j]})
            else: #if the key is not existed
                #else: create a new dict for the key
                new_dict.update({j:{i:new_key[j]}})
    return new_dict
    pass

    #Report: used 2 loops to iterate through the passing value and the key in
    # the dict, create a new dict in dict {x:{y:z}}

################################################################################
# Problem 6: Average the edges in a single state
################################################################################

def average_error_to_weight(error):
    """
    Given the average error of a pollster, returns that pollster's weight.
    The error must be a positive number.
    """
    return error ** (-2)

# The default average error of a pollster who did no polling in the
# previous election.
DEFAULT_AVERAGE_ERROR = 5.0

def pollster_to_weight(pollster, pollster_errors):
    """"
    Given a pollster and a pollster errors, return the given pollster's weight.
    """
    if pollster not in pollster_errors:
        weight = average_error_to_weight(DEFAULT_AVERAGE_ERROR)
    else:
        weight = average_error_to_weight(pollster_errors[pollster])
    return weight


def weighted_average(items, weights):
    """
    Returns the weighted average of a list of items.
    
    Arguments:
    items is a list of numbers.
    weights is a list of numbers, whose sum is nonzero.
    
    Each weight in weights corresponds to the item in items at the same index.
    items and weights must be the same length.
    """
    assert len(items) > 0
    assert len(items) == len(weights)
    #TODO: Implement this function
    #initiate 2 values = 0
    #stote the sum of item * weight
    items_x_weight_total = 0
    #store sum of the weight
    sum_weight = 0
    #for loop iterate through the item
    #i has to be int, cause it also need to iterate through weights
    for i in range(0,len(items)):
        #get one item * weight
        items_x_weight = items[i] * weights[i]
        #store the item * weight into total
        items_x_weight_total += items_x_weight
        #get total sum_weight
        sum_weight += weights[i]
    # caculate average of weighted item
    weight_ave = items_x_weight_total/sum_weight
    return weight_ave
    pass

    #Repost: used a loop to iterate through all items and get their weight
    #use total weight divide by count to get average weight

def average_edge(pollster_edges, pollster_errors):
    """
    Given pollster edges and pollster errors, returns the average of these edges
    weighted by their respective pollster errors.
    """
    #TODO: Implement this function
    #initiate with two new lists
    #store pollster_edges to list
    pollster_edges_list = []
    #store pollster_errors_list to list
    pollster_errors_list = []
    #a new loop to store element into list
    for i in pollster_edges:
        #add each value to pollster_edges_list
        pollster_edges_list.append(pollster_edges[i])
        #get individual weight from pollster_errors
        weight = pollster_to_weight(i,pollster_errors)
        #add each weight to pollster_edges_list
        pollster_errors_list.append(weight)
    #caculate average_edge_score using weighted_average defined earlier
    average_edge_score = weighted_average(pollster_edges_list,pollster_errors_list)
    # round number becasue 4.000000000000001 is causing a problem
    if round(average_edge_score,12) == int(average_edge_score) :
        # if equals retrun the integer value
        average_edge_score = int(average_edge_score)
    return average_edge_score
    pass

    #Report: used a loop to iterate though the pollster_edges
    #use the pollster_to_weight function defined earlier to get the weight
    #use the weighted_average fnction to caculate the average_edge_score

################################################################################
# Problem 7: Predict the 2012 election
################################################################################

def predict_state_edges(pollster_predictions, pollster_errors):
    """
    Given pollster predictions from a current election and pollster errors from
    a past election, returns the predicted state edges of the current election.
    """
    #TODO: Implement this function
    #generate a new dict for state_edges_predict
    state_edges_predict = {}
    #get the pollster_predictions into the correct format
    #use the pivot_nested_dict function defined earlier
    pollster_pre = pivot_nested_dict(pollster_predictions)
    #use a loop to get the items which is nested correctly
    for i in pollster_pre:
        #store each weighted average into the new dict
        state_edges_predict[i]=average_edge(pollster_pre[i], pollster_errors)
        #return the dict
    return state_edges_predict
    pass

    #Report: Finally!!!!!!
    #store the pollster_predictions into the correct dict first
    #used a loop to iterate through the new dict
    #call the average_edge function and store the value into a new dict
    
################################################################################
# Electoral College, Main Function, etc.
################################################################################

def electoral_college_outcome(ec_rows, state_edges):
    """
    Given electoral college rows and state edges, returns the outcome of
    the Electoral College, as a map from "Dem" or "Rep" to a number of
    electoral votes won.  If a state has an edge of exactly 0.0, its votes
    are evenly divided between both parties.
    """
    ec_votes = {}               # maps from state to number of electoral votes
    for row in ec_rows:
        ec_votes[row["State"]] = float(row["Electors"])

    outcome = {"Dem": 0, "Rep": 0}
    for state in state_edges:
        votes = ec_votes[state]
        if state_edges[state] > 0:
            outcome["Dem"] += votes
        elif state_edges[state] < 0:
            outcome["Rep"] += votes
        else:
            outcome["Dem"] += votes/2.0
            outcome["Rep"] += votes/2.0
    return outcome


def print_dict(dictionary):
    """
    Given a dictionary, prints its contents in sorted order by key.
    Rounds float values to 8 decimal places.
    """
    for key in sorted(dictionary.keys()):
        value = dictionary[key]
        if type(value) == float:
            value = round(value, 8)
        print (key, value)


def main():
    """
    Main function, which is executed when election.py is run as a Python script.
    """
    # Read state edges from the 2008 election
    edges_2008 = state_edges(read_csv("./data/2008-results.csv"))
    
    # Read pollster predictions from the 2008 and 2012 election
    polls_2008 = pollster_predictions(read_csv("./data/2008-polls.csv"))
    polls_2012 = pollster_predictions(read_csv("./data/2012-polls.csv"))
    
    # Compute pollster errors for the 2008 election
    error_2008 = pollster_errors(polls_2008, edges_2008)
    
    # Predict the 2012 state edges
    prediction_2012 = predict_state_edges(polls_2012, error_2008)
    
    # Obtain the 2012 Electoral College outcome
    ec_2012 = electoral_college_outcome(read_csv("./data/2012-electoral-college.csv"),
                                        prediction_2012)
    
    print ("Predicted 2012 election results:")
    
    print_dict(prediction_2012)
    print
    
    print ("Predicted 2012 Electoral College outcome:")
    print_dict(ec_2012)
    print    


# If this file, election.py, is run as a Python script (such as by typing
# "python election.py" at the command shell), then run the main() function.
if __name__ == "__main__":
    main()
