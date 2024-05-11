# **Cloud Native Resource REST API in Python on K8s!**

## Development Process

1. Creating REST API in Python using Flask
2. How to run a Python App locally.
3. Containerize the API
    1. Created Dockerfile
    2. Built DockerImage
    3. Ran Docker Container
4. Created ECR repository using Python Boto3 and pushing Docker Image to ECR
5. Used Kubernetes concepts and Created EKS cluster and Nodegroups
6. Created Kubernetes Deployments and Services using Python!


## **Tools** !

(Tools & technologies used in this project)

- [x]  AWS Account.
- [x]  Programmatic access and AWS configured with CLI.
- [x]  Python3 .
- [x]  Docker and Kubectl installed.
- [x]  Code editor (Vscode)

## **Part 1: Deploying the Flask application locally**

### **Step 1: Clone the code**

Clone the code from the repository:

```
git clone berlin_store_locator_api
```

### **Step 2: Install dependencies**

The application uses **`Flask`, and boto3** libraries. Install them using pip:

```
pip3 install -r requirements.txt
```

### **Step 3: Run the application**

To run the application, navigate to the root directory of the project and execute the following command:

```
python3 app.py
```

This will start the Flask server on **`localhost:5000`**. Navigate to [http://localhost:5000/](http://localhost:5000/) on your browser to access the application.

## **Part 2: Dockerized the Flask application**

### **Step 1: Created a Dockerfile**

Create a **`Dockerfile`** in the root directory of the project with the following contents:

### **Step 2: Built the Docker image**

### **Step 3: Ran the Docker container**

This will start the Flask server in a Docker container on **`localhost:5000`**. Navigate to [http://localhost:5000/](http://localhost:5000/) on your browser to access the application.

## **Part 3: Pushed the Docker image to ECR**

### **Step 1: Created an ECR repository**

### **Step 2: Push the Docker image to ECR**

## **Part 4: Creating an EKS cluster and deploying the app using Python**

### **Step 1: Create an EKS cluster**

### **Step 2: Create a node group**

Create a node group in the EKS cluster.

### **Step 3: Create deployment and service**

- Once this file is executed by running “python3 eks.py” deployment and service will be created.
- Confirm by running following commands:

```jsx
kubectl get deployment -n default (check deployments)
kubectl get service -n default (check service)
kubectl get pods -n default (to check the pods)
```

Once the pod is up and running, execute the port-forward to expose the service

```bash
kubectl port-forward service/<service_name> 5000:5000
```
