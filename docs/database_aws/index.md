---
comments: true
---
# How to Set Up a Database and Connect to Your App on an AWS EC2 Instance

If you need to connect to a database, you have two options:

**Option 1:**
Use AWS RDS. It's free for the first year. You can use the free tier for MySQL, PostgreSQL, and MariaDB.

**Option 2:**
Set up a database server on the same EC2 instance. This is not recommended for production but is a good option for development or if you are not expecting a lot of traffic.

## Option 1: Set Up RDS

### Part 1: Setting Up a PostgreSQL Database on AWS RDS

1. **Log in to AWS Management Console:**
    - Open the AWS Management Console and navigate to the RDS service.

2. **Create a New Database Instance:**
    - Click on "Create database."
    - Under Engine options, select PostgreSQL.
    - Choose a template that fits your needs (e.g., Free tier, Production).

3. **Specify DB Details:**
    - DB instance identifier: Provide a unique name for your database instance.
    - Master username & password: Set a strong master username and password. Make sure to note these credentials for later use.

4. **Configure Instance Specifications:**
    - Select an appropriate DB instance class based on performance needs.
    - Allocate storage as needed.

5. **Configure Connectivity:**
    - Virtual Private Cloud (VPC): Choose the VPC where your EC2 instance resides (often the default VPC if you haven't set up a custom one).
    - Public accessibility: For security reasons, if your EC2 is within the same VPC, you can set this to No. If connecting from outside the VPC, set this to Yes.
    - Availability zone: Choose an availability zone that best suits your latency or redundancy requirements.
    - VPC security groups: Either choose an existing security group or create a new one. You will later modify its inbound rules to allow connections from your EC2 instance.

6. **Additional Configuration:**
    - Specify an initial database name if you want RDS to create a database at launch.
    - Configure backup retention, maintenance windows, and monitoring as needed.
    - Click "Create database" at the bottom of the page.

7. **Wait for the Instance to Launch:**
    - It may take a few minutes for the database instance to become available. Once ready, you can see its endpoint and port on the RDS dashboard details page.

### Part 2: Configuring Security Groups

1. **Modify RDS Security Group Inbound Rules:**
    - Navigate to the EC2 console and then to Security Groups.
    - Find the security group associated with your RDS instance (the one selected/created during DB setup).
    - Select Inbound rules and click "Edit inbound rules."
    - Add a rule:
      - Type: PostgreSQL (TCP 5432) or Custom TCP with port 5432.
      - Source: Specify the security group of your EC2 instance or the private IP range of your VPC. Using the security group is recommended for tighter security.
    - Save the changes.

2. **(Optional) Verify VPC and Subnet Settings:**
    - Ensure your EC2 instance and RDS instance are in the same VPC or that there is proper routing between VPCs.
    - Confirm that network ACLs allow traffic on port 5432 between the instances.

### Part 3: Connecting from an EC2 Instance

1. **SSH into Your EC2 Instance:**
    - Use your SSH client to connect to your EC2 instance:
      ```bash
      ssh -i /path/to/your-key.pem ec2-user@<EC2_PUBLIC_DNS_OR_IP>
      ```

2. **Install PostgreSQL Client Tools on EC2:**
    - Depending on your OS, install the PostgreSQL client. For Amazon Linux/CentOS:
      ```bash
      sudo yum install postgresql -y
      ```
    - For Ubuntu/Debian:
      ```bash
      sudo apt-get update
      sudo apt-get install postgresql-client -y
      ```

3. **Test Connection to the RDS PostgreSQL Instance:**
    - Use the `psql` command-line tool to connect. Replace placeholders with your actual values:
      ```bash
      psql --host=<RDS_ENDPOINT> --port=5432 --username=<MASTER_USERNAME> --dbname=<DATABASE_NAME>
      ```
    - When prompted, enter the master password you set during RDS creation.
    - If successful, you'll enter the PostgreSQL interactive terminal.

4. **Troubleshoot Connection Issues:**
    - If you cannot connect, verify:
      - The RDS endpoint and port are correct.
      - Security groups allow inbound traffic on port 5432 from the EC2 instance.
      - The EC2 instance can reach the RDS endpoint (you can use tools like `telnet <RDS_ENDPOINT> 5432` or `nc -zv <RDS_ENDPOINT> 5432` to test connectivity).
      - There are no network ACLs blocking the connection.

### Part 4: Using the Database in Your Applications

1. **Store Connection Details Securely:**
    - Use environment variables or secure storage to store your DB credentials and connection details, rather than hardcoding them in your application.

2. **Connect Using a Database Library/ORM:**
    - In your application code running on EC2, use the appropriate PostgreSQL driver or ORM to establish a connection using the RDS endpoint, port, database name, username, and password. For example, in Python using `psycopg2`:
      ```python
      import psycopg2

      conn = psycopg2.connect(
            host="<RDS_ENDPOINT>",
            port=5432,
            dbname="<DATABASE_NAME>",
            user="<MASTER_USERNAME>",
            password="<YOUR_PASSWORD>"
      )
      ```
    - Replace placeholders with actual values.

3. **Perform Database Operations:**
    - Once connected, you can run SQL queries, create tables, insert data, etc., from your application or using the `psql` CLI tool.

## Option 2: Set Up PostgreSQL on the EC2 Instance

### Part 1: Launching and Preparing Your EC2 Instance

1. **Launch an EC2 Instance:**
    - From the AWS Management Console, navigate to EC2 and launch a new instance.
    - Choose an Amazon Machine Image (AMI) that suits your needs, such as Amazon Linux 2, Ubuntu, or another supported distribution.
    - Configure instance details, add storage, and assign a security group that allows SSH (port 22) connections. You may later open port 5432 if you need remote DB access.
    - Launch the instance with a key pair for SSH access.

2. **SSH into Your EC2 Instance:**
    - Use your terminal or SSH client to connect:
      ```bash
      ssh -i /path/to/your-key.pem ec2-user@<EC2_PUBLIC_DNS_OR_IP>
      ```
    - (Replace `ec2-user` with `ubuntu` for Ubuntu AMIs, etc.)

### Part 2: Installing PostgreSQL on the EC2 Instance

1. **For Amazon Linux 2 / RHEL/CentOS:**

    - **Update Packages:**
      ```bash
      sudo yum update -y
      ```

    - **Install PostgreSQL:**
      ```bash
      sudo yum install -y postgresql-server postgresql-contrib
      ```

    - **Initialize PostgreSQL Database:**
      ```bash
      sudo postgresql-setup initdb
      ```

    - **Start PostgreSQL Service:**
      ```bash
      sudo systemctl start postgresql
      sudo systemctl enable postgresql
      ```

2. **For Ubuntu/Debian:**

    - **Update Packages:**
      ```bash
      sudo apt-get update
      ```

    - **Install PostgreSQL:**
      ```bash
      sudo apt-get install -y postgresql postgresql-contrib
      ```

    - **Ensure PostgreSQL is Running:**
      ```bash
      sudo systemctl start postgresql
      sudo systemctl enable postgresql
      ```

### Part 3: Configuring PostgreSQL

1. **Edit PostgreSQL Configuration (if needed):**
    - The primary configuration file is usually located at:
      - Amazon Linux/RHEL/CentOS: `/var/lib/pgsql/data/postgresql.conf`
      - Ubuntu/Debian: `/etc/postgresql/<version>/main/postgresql.conf`
    - **Listening Addresses:**
      - By default, PostgreSQL listens only on localhost. If your application resides on the same EC2 or you require external connections, update the `listen_addresses` line:
         ```conf
         listen_addresses = '*'
         ```
      - Save the file after making changes.

2. **Configure Client Authentication:**
    - Edit the `pg_hba.conf` file to control which hosts can connect and how they authenticate:
      - Amazon Linux/RHEL/CentOS: `/var/lib/pgsql/data/pg_hba.conf`
      - Ubuntu/Debian: `/etc/postgresql/<version>/main/pg_hba.conf`
    - For local connections, the default configuration is typically sufficient. For remote access, add lines like:
      ```conf
      host    all    all    0.0.0.0/0    md5
      ```
    - **Security Note:** Using `0.0.0.0/0` opens access from any IP address. For security, restrict this to specific IP ranges or networks as needed.

3. **Restart PostgreSQL to Apply Changes:**
    ```bash
    sudo systemctl restart postgresql
    ```

### Part 4: Creating Database Users and Databases (Credentials Setup)

1. **Switch to the PostgreSQL User:**
    ```bash
    sudo -i -u postgres
    ```

2. **Access the PostgreSQL Shell:**
    ```bash
    psql
    ```

3. **Create a New Database User and Database:**
    - Create a user: Replace `<username>` and `<password>` with your desired credentials.
      ```sql
      CREATE USER <username> WITH PASSWORD '<password>';
      ```
    - Create a database: Replace `<dbname>` with your database name.
      ```sql
      CREATE DATABASE <dbname> OWNER <username>;
      ```

4. **Set User Privileges (if needed):**
    - For example, to grant all privileges on the database to the user:
      ```sql
      GRANT ALL PRIVILEGES ON DATABASE <dbname> TO <username>;
      ```

5. **Exit the `psql` shell and `postgres` user:**
    ```sql
    \q
    exit
    ```

6. **Note on Credentials:**
    - The credentials for your database server consist of:
      - Username: The PostgreSQL user you created.
      - Password: The password you assigned to that user.
      - Database Name: The database you created.
      - Host: For connections from the same EC2 instance, use `localhost` or `127.0.0.1`. For remote connections, use the EC2 instance's public or private IP (if within the same VPC).
      - Port: Default PostgreSQL port 5432 (unless configured otherwise).

7. **Storing Credentials Securely:**
    - Do not hardcode credentials into your application source code. Instead, store them in environment variables, configuration files with restricted permissions, or use AWS services like AWS Secrets Manager for secure storage.

### Part 5: Connecting Your Application to the PostgreSQL Database

1. **Install PostgreSQL Client Libraries in Your Application Environment:**
    - Ensure that the environment where your application runs (which may also be the same EC2 instance or a different one) has the appropriate PostgreSQL client libraries or drivers installed for your programming language/framework.

2. **Construct the Database Connection String:**
    - The connection string will typically look like this:
      ```php
      postgresql://<username>:<password>@<host>:<port>/<dbname>
      ```
    - Example:
      ```bash
      postgresql://myuser:mypassword@localhost:5432/mydatabase
      ```

3. **Configure Your Application:**
    - Update your application's database configuration to use the connection string or individual connection parameters (host, port, database, username, password) that you created.
    - For instance, in a Python application using SQLAlchemy, you might set:
      ```python
      SQLALCHEMY_DATABASE_URI = 'postgresql://myuser:mypassword@localhost:5432/mydatabase'
      ```
    - For Node.js with `pg` library:
      ```javascript
      const { Client } = require('pg');
      const client = new Client({
         host: 'localhost',
         port: 5432,
         user: 'myuser',
         password: 'mypassword',
         database: 'mydatabase'
      });
      client.connect();
      ```

4. **Test the Database Connection:**
    - Run your application and perform a test query or use a database client library to ensure the application can successfully connect to PostgreSQL and perform operations.

### Additional Tips:

1. **Firewall and Security Groups:**
    - If your application connects remotely to the PostgreSQL server, ensure the EC2 instance's security group allows inbound traffic on port 5432 from the application’s IP or network.

2. **Managing Database Credentials:**
    - **Environment Variables:** You can set environment variables on the EC2 instance or application server to store credentials securely. For example, in Linux:
      ```bash
      export DB_USER=myuser
      export DB_PASSWORD=mypassword
      export DB_NAME=mydatabase
      export DB_HOST=localhost
      export DB_PORT=5432
      ```
    - **Configuration Files:** Store credentials in a config file with restricted permissions (e.g., using Linux file permissions `chmod 600 config.file`).
    - **AWS Secrets Manager:** For improved security, consider storing credentials in AWS Secrets Manager and retrieving them programmatically within your application.

3. **Securing PostgreSQL:**
    - Regularly update PostgreSQL.
    - Use strong passwords for database users.
    - Limit network exposure by properly configuring `pg_hba.conf` and security groups.