import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    months ={
	'Jan':0,
	'Feb':1,
	'Mar':2,
	'Apr':3,
	'May':4,
	'June':5,
	'Jul':6,
	'Aug':7,
	'Sep':8,
	'Oct':9,
	'Nov':10,
	'Dec':11

    }

    evidence = []
    labels = []
    try:
        file = open(filename)
    except FileNotFoundError:
        print("File donot exists")
        return


    
    csvreader = csv.DictReader(file)
    header = next(csvreader)


    for row in csvreader:
        evidence.append([
            int(row['Administrative']),
            float(row['Administrative_Duration']),
            int(row['Informational']),
            float(row['Informational_Duration']),
            int(row['ProductRelated']),
            float(row['ProductRelated_Duration']),
            float(row['BounceRates']),
            float(row['ExitRates']),
            float(row['PageValues']),
            float(row['SpecialDay']),
            months[row['Month']],
            int(row['OperatingSystems']),
            int(row['Browser']),
            int(row['Region']),
            int(row['TrafficType']),
            1 if row['VisitorType'] == 'Returning_Visitor' else 0,
            1 if row['Weekend'] == 'TRUE' else 0
        ])
        
        labels.append(1 if row['Revenue'] == 'TRUE' else 0)
    
    return (evidence,labels)



def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    neigh = KNeighborsClassifier(n_neighbors=1)
    neigh.fit(evidence,labels)
    return neigh
    


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    count_neg =0
    count_pos =0
    total_pos =0
    total_neg =0
    for index, (value1, value2) in enumerate(zip(labels, predictions)):
        if value1 ==1:
            total_pos =total_pos+1
            if value1 ==value2:
                count_pos =count_pos+1
            
        else:
            total_neg =total_neg+1
            if value1 ==value2:
                count_neg =count_neg+1
        

    return (float(count_pos)/total_pos,float(count_neg)/total_neg)
    

if __name__ == "__main__":
    main()
