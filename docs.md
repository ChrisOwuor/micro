# Microfinance API Documentation

## Introduction

Welcome to the Microfinance API designed to facilitate seamless communication between financial services and other microfinance institutions or related entities. This documentation provides an overview of the API's features, endpoints, and usage guidelines.

### API Base URL

`https://api.visionfundmicrofinance.com`

## 1. User Management

### 1.1 Create client Profile

**Endpoint:**

`POST /users`

**Description:**

Create a new client profile with personal details.

**Request:**

```json
{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "role": "client",
  "id_number":"1234567"
}
```

**Response:**

``` json
{
  "id": 123,
  "name": "John Doe",
  "email": "john.doe@example.com",
  "role": "client",
//   generated acount number
  "a/c":"john1234567",
}
```

### 1.2 Create user Profile

**Endpoint:**

`POST /users`

**Description:**

Create a new user profile with personal details.

**Request:**

```json
{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "role": "user",
}
```

**Response:**

``` json
{
  "id": 123,
  "name": "John Doe",
  "email": "john.doe@example.com",
  "role": "user",
//   generated acount number
}
```

### 1.3 Authentication

**Endpoint:**

`POST /auth/token`

**Description:**

Obtain an authentication token for API access.

**Request:**

```json
{
  "username": "john.doe@example.com",
  "password": "securepassword"
}
```

**Response:**

```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}

```

## 2. Transaction Handling

### **Transactions by client**

* ### Client Withdrawals

* ### Client Deposit

* ### Client Loan Repayment

### **Transactions by user**

* ### loan disbursment to either mpesa or account

### 2.1 All Transactions by  for an individual client

**Endpoint:**

`POST api/transactions/{client_id}`

**Description:**

Record a financial transaction for a client

**Request:**

``` json
{
  "token": "q1w2e3r4t5t65",
}
```

**Response:**

``` json
{
  "id": 456,
  "code":"qwerty12",
  "user_id": 123,
  "amount": 100.00,
  "type": "withdrawal / deposit / loan repayment ",
  "time":"12:23:45",
  "date":"2/3/2024"


}
```

### 2.1 loan disbursment transaction

**Endpoint:**

`POST api/transactions/disburse/{client_id}`

**Description:**

Make  loan disbursment to a client

**Request:**

``` json
{
  "amount":233,
  "user_token": "q1w2e3r4t5t65",
}
```

**Response:**.

``` json
{
  "id": 456,
  "by":"user_id",
  "code":"qwerty12",
  "user_id": 123,
  "amount": 233.00,
  "type": "disbursement",
  "time":"12:23:45",
  "date":"2/3/2024"

}
```

### 2.3 loan repayment by client transaction

**Endpoint:**

`POST api/transactions/loans/repayment/{client_id}`

**Description:**

Make  loan repayment by a client

**Request:**

``` json
{
"source":"mpesa /account",
  "amount":233,
  "client_token": "q1w2e3r4t5t65",
}
```

**Response:**.

``` json
{
  "id": 456,
  "code":"qwerty12",
  "amount": 233.00,
  "time":"12:23:45",
  "date":"2/3/2024",
  "balance":"289"

}
```

### 2.4 client deposit transaction

**Endpoint:**

`POST api/transactions/deposit/{client_id}`

**Description:**

Make  a deposit transaction by a client

**Request:**

``` json
{
"source":"mpesa",
  "amount":233,
  "client_token": "q1w2e3r4t5t65",
}
```

**Response:**.

``` json
{
  "id": 456,
  "code":"qwerty12",
  "time":"12:23:45",
  "date":"2/3/2024",
  "balance":"22"

}
```

### 2.5 client withdrawal transaction

**Endpoint:**

`POST api/transactions/deposit/{client_id}`

**Description:**

Make  a withdrawal transaction by a client

**Request:**

``` json
{
  "amount":233,
  "client_token": "q1w2e3r4t5t65",
}
```

**Response:**.

``` json
{
  "id": 456,
  "code":"qwerty12",
  "time":"12:23:45",
  "date":"2/3/2024",
  "balance":"22"

}
```

## 3. Loan Information

### **Loan information types**

* ### get all loans by client

* ### get pending loans by client

* ### get all loans both pending and previous for a single client by the third party

### 3.1 Loan Details

**Endpoint:**

`GET /loans/{user_id}`

**Description:**

Retrieve loan details for a specific user.

**Request:**

``` json
{
  "client_token": "q1w2e3r4t5t65",
}
```

**Response:**

``` json
{
  "user_id": 123,
  "loan_amount": 5000.00,
  "repayment_schedule": "monthly",
  "outstanding_amount": 2500.00,
  "status": "approved"
}
```
