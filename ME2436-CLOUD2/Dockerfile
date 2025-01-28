# Χρήση της Python ως βάση
FROM python:3.11-slim

# Ορίζουμε τον φάκελο εργασίας μέσα στο container
WORKDIR /app

# Αντιγράφουμε όλα τα αρχεία του φακέλου στον φάκελο /app του container
COPY . .

# Εγκατάσταση απαιτούμενων βιβλιοθηκών
RUN pip install -r requirements.txt

# Ορίζουμε την εντολή που θα τρέχει το αρχείο Python
CMD ["python", "table_app.py"]