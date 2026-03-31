# Setup & Run Instructions

## 1. Provision AWS Resources

- Create an **EC2 instance**
- Create an **S3 bucket** (optional, for storing output)
- (Optional) Attach an IAM role with S3 access to the EC2 instance

---

## 2. Connect to EC2

```bash
ssh -i <your-key.pem> ubuntu@<your-ec2-ip>
```

---

## 3. Install Git

```bash
sudo apt update
sudo apt install git -y
```

---

## 4. Clone the Repository

```bash
git clone https://github.com/mzowera/relx_screening.git
cd relx_screening
```

---

## 5. Install Python & Pip

```bash
sudo apt install python3 python3-pip -y
```

---

## 6. Install Dependencies

```bash
pip3 install -r requirements.txt
```

> If `requirements.txt` is not available:

```bash
pip3 install requests beautifulsoup4 boto3 schedule
```

---

## 7. Run the Activity Script

```bash
python3 activity*.py
```

## Note

- I used schedule package to easily demonstrate the scheduling
