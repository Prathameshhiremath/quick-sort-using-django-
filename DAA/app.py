from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import random
import time

app = Flask(__name__, static_url_path='/static')

# Replace these with your own database credentials
host = 'localhost'
user = 'root'
password = 'Prathamesh@2001'
database = 'college'


def fetch_register_numbers_from_database():
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        if connection.is_connected():
            cursor = connection.cursor()
            query = "SELECT usn FROM studentinfo"
            cursor.execute(query)
            my_list = [row[0] for row in cursor.fetchall()]
            return my_list

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

    return []

def partition(arr, low, high):
    pivot = arr[low]
    left = low + 1
    right = high
    done = False

    while not done:
        while left <= right and arr[left] <= pivot:
            left = left + 1
        while arr[right] >= pivot and right >= left:
            right = right - 1
        if right < left:
            done = True
        else:
            arr[left], arr[right] = arr[right], arr[left]

    arr[low], arr[right] = arr[right], arr[low]
    return right

def quick_sort(arr, low, high):
    if low < high:
        pivot_index = partition(arr, low, high)
        quick_sort(arr, low, pivot_index - 1)
        quick_sort(arr, pivot_index + 1, high)

def randomized_partition(arr, low, high):
    pivot_index = random.randint(low, high)
    arr[low], arr[pivot_index] = arr[pivot_index], arr[low]
    return partition(arr, low, high)

def randomized_quick_sort_helper(arr, low, high):
    if low < high:
        pivot_index = randomized_partition(arr, low, high)
        randomized_quick_sort_helper(arr, low, pivot_index - 1)
        randomized_quick_sort_helper(arr, pivot_index + 1, high)

def randomized_quick_sort(arr):
    randomized_quick_sort_helper(arr, 0, len(arr) - 1)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sort', methods=['POST'])
def sort():
    choice = int(request.form['choice'])
    my_list = fetch_register_numbers_from_database()

    if choice == 1:
        start_time = time.perf_counter() * 1000000
        quick_sort(my_list, 0, len(my_list) - 1)
        end_time = time.perf_counter() * 1000000
        sorted_list = my_list
        sort_time = end_time - start_time
        return render_template('sorted_list.html', sorted_list=sorted_list, sort_time=sort_time, technique='Quick Sort')
    
    elif choice == 2:
        start_time = time.perf_counter() * 1000000
        randomized_quick_sort(my_list)
        end_time = time.perf_counter() * 1000000
        sorted_list = my_list
        sort_time = end_time - start_time
        return render_template('sorted_list.html', sorted_list=sorted_list, sort_time=sort_time, technique='Randomized Quick Sort')

    return redirect(url_for('index'))

@app.route('/fetch', methods=['GET'])
def fetch():
    register_numbers = fetch_register_numbers_from_database()
    if register_numbers:
        return render_template('register_numbers.html', register_numbers=register_numbers)
    else:
        return "No data retrieved from the database."

if __name__ == "__main__":
    app.run(debug=True)
