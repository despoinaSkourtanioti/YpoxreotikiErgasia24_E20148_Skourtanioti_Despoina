# YpoxreotikiErgasia24_E20148_Skourtanioti_Despoina

# Τεχνολογίες:

Python, Microframework Flask, Docker, MongoDB, HTML

# Περιγραφή Αρχείων:

docker-compose.yml συνδέει τα container του server και της βάσης δεδομένων
Dockerfile για τη δημιουργία image
initialize_db.py για την προσθήκη του admin στο db αν δεν είναι ήδη
run.py api με τα route
requirements.txt τα requirements για να τρέξει το run.py
app file με τα templates (HTML)

# Τρόπος Εκτέλεσης:

1. Download των αρχείων
2. Extract των αρχείων
3. CMD: CD στο directory του hospital_management
4. ```docker-compose up --build```
5. Σε ένα browser: localhost:5000

# Τρόπος Χρήσης:

Υπάρχουν 4 collection:
1. users (RBAC)
2. doctors
3. patients
4. appointments

Admin credentials:
Username: admin
password: @dm1n

Λειτουργικότητες User:
1. login
2. logout

Λειτουργικότητες Admin:
1. δημιουργία doctor
2. αλλαγή κωδικού doctor
3. διαγραφή doctor
4. διαγραφή patient

Λειτουργικότητες Doctor:
1. αλλαγή κωδικού
2. αλλαγή κόστους
3. διαγραφή doctor
4. προβολή ραντεβού

Λειτουργικότητες Patient:
1. εγγραφη
2. αναζήτηση ραντεβού
3. κράτηση ραντεβού
4. προβολή ραντεβού
5. ακύρωση ραντεβού

# Screenshots:

Home:
![Screenshot (376)](https://github.com/despoinaSkourtanioti/YpoxreotikiErgasia24_E20148_Skourtanioti_Despoina/assets/137726116/a75eeb01-0426-493a-8802-c8ae520c9f94)
Admin Dashboard:
![Screenshot (377)](https://github.com/despoinaSkourtanioti/YpoxreotikiErgasia24_E20148_Skourtanioti_Despoina/assets/137726116/66980d60-d4b0-4605-9a52-aee4add86361)
Δημιουργία doctor:
![Screenshot (378)](https://github.com/despoinaSkourtanioti/YpoxreotikiErgasia24_E20148_Skourtanioti_Despoina/assets/137726116/a00668fa-22e5-4350-bd32-a4640d4ddaeb)
Doctor Dashboard:
![Screenshot (379)](https://github.com/despoinaSkourtanioti/YpoxreotikiErgasia24_E20148_Skourtanioti_Despoina/assets/137726116/6c833e9f-1044-4734-98e1-2db2cd62686c)
Αλλαγή κόστους:
![Screenshot (380)](https://github.com/despoinaSkourtanioti/YpoxreotikiErgasia24_E20148_Skourtanioti_Despoina/assets/137726116/89e0ee66-365e-4714-b6f0-dd7a9735b7f0)
Register:
![Screenshot (381)](https://github.com/despoinaSkourtanioti/YpoxreotikiErgasia24_E20148_Skourtanioti_Despoina/assets/137726116/edeeba9d-2bcc-45b7-9a98-1cf97442fff3)
Patient Dashboard:
![Screenshot (55)](https://github.com/user-attachments/assets/7ccf136f-74b1-412b-8049-84fbeae25f69)
Αναζήτηση ραντεβού
![Screenshot (383)](https://github.com/despoinaSkourtanioti/YpoxreotikiErgasia24_E20148_Skourtanioti_Despoina/assets/137726116/81244650-55c4-4cad-a4ed-0fb09d3e7a9d)
Κράτηση ραντεβού
![Screenshot (384)](https://github.com/despoinaSkourtanioti/YpoxreotikiErgasia24_E20148_Skourtanioti_Despoina/assets/137726116/d28e4365-67b2-4f2d-8dd3-c1286812889f)
Προβολή λεπτομερειών ραντεβού:
![Screenshot (386)](https://github.com/despoinaSkourtanioti/YpoxreotikiErgasia24_E20148_Skourtanioti_Despoina/assets/137726116/38754e2d-135b-4e75-8277-e0b22b51f751)
Προβολή ραντεβού signed in ως doctor:
![Screenshot (387)](https://github.com/despoinaSkourtanioti/YpoxreotikiErgasia24_E20148_Skourtanioti_Despoina/assets/137726116/c4313310-8a80-480c-afdd-bf898cc89e7c)
Μετά τη διαγραφή του doctor από τον admin η προβολή ραντεβού signed in ως patient:
![Screenshot (388)](https://github.com/despoinaSkourtanioti/YpoxreotikiErgasia24_E20148_Skourtanioti_Despoina/assets/137726116/5cb9ed23-b757-46f8-95fa-1da13c8a7947)
