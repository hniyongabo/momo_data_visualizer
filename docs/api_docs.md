# **MoMo SMS Transaction API Documentation**

## **Base URL**

`http://localhost:8000/transactions`

---

## **Authentication**

All endpoints require **Basic Authentication**.

**Headers:**

`Authorization: Basic <base64_encoded_credentials>`

**Example:**

* Username: `admin`

* Password: `password123`

* Base64: `YWRtaW46cGFzc3dvcmQxMjM=`

⚠️ Note: Basic Auth is weak. Credentials are sent in every request and can be intercepted if HTTPS is not used. In production, JWT or OAuth2 would be better.

---

## **Data Source**

**File:** `modified_sms_v2.xml`

Example snippet from XML:

`<smses count="2">`  
  `<sms protocol="0" address="John Doe" date="1737023646162" type="1">`  
    `<transaction type="deposit" amount="10000" sender="John Doe" receiver="MoMo Account" timestamp="2025-01-15T10:30:00"/>`  
  `</sms>`  
  `<sms protocol="0" address="Jane Smith" date="1737027654321" type="2">`  
    `<transaction type="withdrawal" amount="5000" sender="MoMo Account" receiver="Jane Smith" timestamp="2025-01-15T11:45:00"/>`  
  `</sms>`  
`</smses>`

After parsing, the JSON objects look like this:

`[`  
     `"transaction": {`  
      `"transaction_id": "43668074924",`  
      `"user_id": 6,`  
      `"transaction_date": "2024-05-14T18:58:35.618000+00:00",`  
      `"toa": "null",`  
      `"sc_toa": "null",`  
      `"readable_date": "14 May 2024 8:58:35 PM",`  
      `"amount": 25000.0,`  
      `"status": "COMPLETED",`  
      `"service_center_number": "+250788110381",`  
      `"sender_name": "Samuel Carter"`  
    `},`  
  	`"transaction": {`  
      `"transaction_id": "2024-05-14T17:21:24.404000+00:00#20",`  
      `"user_id": 6,`  
      `"transaction_date": "2024-05-14T17:21:24.404000+00:00",`  
      `"toa": "null",`  
      `"sc_toa": "null",`  
      `"readable_date": "14 May 2024 7:21:24 PM",`  
      `"amount": 1800.0,`  
      `"status": "COMPLETED",`  
      `"service_center_number": "+250788110381",`  
      `"sender_name": null`  
    `},`  
`]`

---

## **Transactions API**

### **1\. GET /transactions**

Get all transactions or filter by type, sender, receiver, or amount.

**Request Example:**

`curl -X GET http://localhost:8000/transactions -u admin:password123`

**Response Example:**

`{`  
  `"status": 200,`  
  `"message": "success",`  
  `"data": [ ... ],  // JSON data from parsed XML`  
  `"count": 2`  
`}`

**Errors:**

* 401 Unauthorized: wrong/missing credentials

* 400 Bad Request: invalid query params

---

### **2\. GET /transactions/{id}**

Get one transaction by ID.

**Request Example:**

`curl -X GET http://localhost:8000/transactions/0001 -u admin:password123`

**Response Example:**

`{`  
  `"status": 200,`  
  `"message": "success",`  
  `"data": {`  
      `"transaction_id": "2024-05-14T17:21:24.404000+00:00#20",`  
      `"user_id": 6,`  
      `"transaction_date": "2024-05-14T17:21:24.404000+00:00",`  
      `"toa": "null",`  
      `"sc_toa": "null",`  
      `"readable_date": "14 May 2024 7:21:24 PM",`  
      `"amount": 1800.0,`  
      `"status": "COMPLETED",`  
      `"service_center_number": "+250788110381",`  
      `"sender_name": null`  
    `}`  
`}`

**Errors:**

* 404 Not Found if ID doesn’t exist

* 400 Bad Request if ID missing/invalid

---

### **3\. POST /transactions**

Create a new transaction.

**Request Example:**

`curl -X POST http://localhost:8000/transactions \`  
`-u admin:password123 \`  
`-H "Content-Type: application/json" \`  
`-d '{`  
      `"transaction_id": "2024-05-14T17:21:24.404000+00:00#20",`  
      `"user_id": 6,`  
      `"transaction_date": "2024-05-14T17:21:24.404000+00:00",`  
      `"toa": "null",`  
      `"sc_toa": "null",`  
      `"readable_date": "14 May 2024 7:21:24 PM",`  
      `"amount": 1800.0,`  
      `"status": "COMPLETED",`  
      `"service_center_number": "+250788110381",`  
      `"sender_name": null`  
    `}'`

**Response Example:**

`{`  
  `"status": 201,`  
  `"message": "transaction created successfully",`  
  `"data": {`  
      `"transaction_id": "2024-05-14T17:21:24.404000+00:00#20",`  
      `"user_id": 6,`  
      `"transaction_date": "2024-05-14T17:21:24.404000+00:00",`  
      `"toa": "null",`  
      `"sc_toa": "null",`  
      `"readable_date": "14 May 2024 7:21:24 PM",`  
      `"amount": 1800.0,`  
      `"status": "COMPLETED",`  
      `"service_center_number": "+250788110381",`  
      `"sender_name": null`  
    `}`  
`}`

**Errors:**

* 400 Bad Request if required fields are missing

---

### **4\. PUT /transactions/{id}**

Update a transaction.

**Request Example:**

`curl -X PUT http://localhost:8000/transactions/0003 \`  
`-u admin:password123 \`  
`-H "Content-Type: application/json" \`  
`-d '{"amount": 8000}'`

**Response Example:**

`{`  
  `"status": 200,`  
  `"message": "transaction with id 0003 updated successfully",`  
  `"data": { ... }`  
`}`

**Errors:**

* 404 Not Found if ID doesn’t exist

* 400 Bad Request if no fields are provided

---

### **5\. DELETE /transactions/{id}**

Delete a transaction.

**Request Example:**

`curl -X DELETE http://localhost:8000/transactions/0003 -u admin:password123`

**Response Example:**

`{`  
  `"status": 200,`  
  `"message": "transaction with id 0003 has been deleted successfully"`  
`}`

**Errors:**

* 404 Not Found if ID doesn’t exist

---

## **Error Codes Summary**

| Code | Meaning | When it occurs |
| ----- | ----- | ----- |
| 200 | OK | Successful GET, PUT, DELETE |
| 201 | Created | Resource successfully created |
| 400 | Bad Request | Missing/invalid parameters |
| 401 | Unauthorized | Wrong/missing credentials |
| 404 | Not Found | Resource doesn’t exist |
| 500 | Internal Server Error | Server errors |

---

## **Security Considerations**

* **Basic Auth limitations:** Credentials are sent with every request, Base64 encoding is not secure, and no token expiration.

* **Recommendations for production:** Use HTTPS, implement JWT/OAuth2, validate inputs, and enable logging & monitoring.

---

## **API Versioning**

* Current version: `v1`

* Future structure: `http://localhost:8000/api/v1/transactions`

