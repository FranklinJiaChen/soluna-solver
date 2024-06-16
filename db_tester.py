import mysql.connector

# MySQL connection configuration
config = {
    'user': 'root',
    'host': 'localhost',
    'database': 'soluna',
}

def get_column_names(table_name):
    """
    Retrieve column names of a specific table in MySQL database.
    """
    try:
        # Connect to MySQL
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # Query to retrieve column names
        query = f"SHOW COLUMNS FROM {table_name}"
        cursor.execute(query)

        # Fetch all column names
        columns = cursor.fetchall()
        column_names = [column[0] for column in columns]

        return column_names

    except mysql.connector.Error as e:
        print(f"Error retrieving column names: {e}")
        return None

    finally:
        # Close cursor and connection
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print('MySQL connection closed')

def test_mysql_connection():
    """
    Test MySQL database connection and basic operations.
    """
    try:
        # Connect to MySQL
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # Check if connection is successful
        if conn.is_connected():
            print('Connected to MySQL database')

            # Example: Inserting data into soluna table
            cursor.execute('INSERT INTO soluna (state, eval) VALUES ("[[1, 1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1]]", 0)')
            conn.commit()
            print("Data inserted successfully")

            # Example: Querying data from soluna table
            cursor.execute("SELECT * FROM soluna")
            results = cursor.fetchall()
            print("soluna Table Contents:")
            for row in results:
                print(row)

            # Fetch specific board configuration
            board_key = [[1, 1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1]]
            cursor.execute(f"SELECT * FROM soluna WHERE state = '{board_key}'")
            # cursor.execute("SELECT * FROM soluna WHERE state = 'na'")
            board_data = cursor.fetchone()

            if board_data:
                print("Board configuration retrieved successfully:")
                print(board_data)
            else:
                print("Board configuration not found.")

            # Example: Retrieve column names of soluna table
            columns = get_column_names('soluna')
            if columns:
                print(f"\nColumn names of table 'soluna':")
                print(columns)

    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")

    finally:
        # Close cursor and connection
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print('MySQL connection closed')

if __name__ == '__main__':
    test_mysql_connection()
