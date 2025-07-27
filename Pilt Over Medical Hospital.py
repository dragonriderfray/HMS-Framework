#Hospital Management System
#---------------------------------------------------------------------------------------------------------------------
#Importing necessary modules
import random
import string
from datetime import datetime
#---------------------------------------------------------------------------------------------------------------------
#Function to generate unique IDs
def generate_id(prefix):
    return f"{prefix}{random.randint(10000, 99999)}"

#A function to check doctor's schedule for availability
def is_time_available(schedule, date, time):
    return (date, time) not in schedule

#---------------------------------------------------------------------------------------------------------------------
#Creating Person Class (Parent Class)
class Person:
    def __init__(self, name, age, gender, dateofbirth):
        self.name = name
        self.age = age
        self.gender = gender
        self.dateofbirth = dateofbirth

    def display_info(self):
        print(f"Name: {self.name}")
        print(f"Age: {self.age}")
        print(f"Gender: {self.gender}")
        print(f"Date Of Birth: {self.dateofbirth}")

#---------------------------------------------------------------------------------------------------------------------
#Creating Patient Class (Inherits Person Class)
class Patient(Person):
    def __init__(self, name, age, gender,dateofbirth):
        super().__init__(name, age, gender,dateofbirth)
        self.patient_id = generate_id("P")
        self.appointment_list = []

#This method displays the patient's profile
    def profile_display(self):
        print("\n------------Patient File-------------")
        print(f"Patient ID: {self.patient_id}")
        self.display_info()
        print("---------------------------------------\n")

#This method updates the patient's appointments
    def book_appointment(self, appointment):
        self.appointment_list.append(appointment)

#---------------------------------------------------------------------------------------------------------------------
#Creating Doctor Class (Inherits Person Class)
class Doctor(Person):
    def __init__(self, name, age, gender, dateofbirth, speciality):
        super().__init__(name, age, gender, dateofbirth)
        self.doctor_id = generate_id("DR")
        self.speciality = speciality
        self.schedule = []

#This method passes is_time_available function through it
    def is_available(self, date, time):
        return is_time_available(self.schedule, date, time)

#This method displays the doctor's schedule
    def view_schedule(self):
        print(f"Schedule for Dr. {self.name}")
        if self.schedule:
            for date, time in self.schedule:
                print(f"{date} at {time}\n")
        else:
            print("There are no times available\n")

#---------------------------------------------------------------------------------------------------------------------
#Creating Nurse Class (Inherits Person Class)
class Nurse(Person):
    def __init__(self, name, age, gender, dateofbirth):
        super().__init__(name, age, gender, dateofbirth)
        self.nurse_id = generate_id("NR")
        self.assigned_patients = []

#This method updates the nurse's list of patients
    def assign_patient(self, patient):
        self.assigned_patients.append(patient)

#This method views all the patients to a nurse
    def view_assigned_patients(self):
        print(f"\nPatients assigned to Nurse {self.name}:")
        if self.assigned_patients:
            for patient in self.assigned_patients:
                print(f"- {patient.name} (ID: {patient.patient_id})")
        else:
            print("No patients assigned.")

#---------------------------------------------------------------------------------------------------------------------
#Creating Appointment Class
class Appointment:
    appointment_counter = 1

    def __init__(self, patient, doctor, nurse, date, time):
        self.appointment_id = generate_id("APT")
        self.patient = patient
        self.doctor = doctor
        self.nurse = nurse
        self.date = date
        self.time = time

#This method displays confirmed appointment date and time
    def confirmed(self):
        print("\n*Appointment confirmed")
        print(f"Appointment ID: {self.appointment_id}")
        print(f"The appointment set for {self.date} at {self.time}.")

#This method displays canceled appointment
    def cancel(self):
        self.status = "Appointment Canceled"
        print(f"\nAppointment {self.appointment_id} has been canceled\n")

#---------------------------------------------------------------------------------------------------------------------
#Creating Hospital Management System Class
#Allows registration for patients, doctors and nurses, setting, canceling appointments and creating an invoice
class HospitalManagement:
    def __init__(self):
        self.patient = {}
        self.doctor = {}
        self.nurse = {}
        self.appointment = {}

#This method adds a patient
    def add_patient(self, name, age, gender, dateofbirth):
        patient = Patient(name, age, gender, dateofbirth)
        self.patient[patient.patient_id] = patient
        print(f"\n*Patient registered successfully")
        print(f"Patient ID: >>{patient.patient_id}<<\n")

# his method adds a doctor
    def add_doctor(self, name, age, gender, dateofbirth, speciality):
        doctor = Doctor(name, age, gender, dateofbirth, speciality)
        self.doctor[doctor.doctor_id] = doctor
        print(f"\n*Doctor registered successfully")
        print(f"Doctor ID: >>{doctor.doctor_id}<<\n")

#This method adds a nurse
    def add_nurse(self, name, age, gender, dateofbirth):
        nurse = Nurse(name, age, gender, dateofbirth)
        self.nurse[nurse.nurse_id] = nurse
        print(f"\n*Nurse registered successfully")
        print(f"Nurse ID: >>{nurse.nurse_id}<<\n")

#This method assigns a nurse to a patient
    def assign_nurse_to_patient(self, patient):
        for nurse in self.nurse.values():
         if len(nurse.assigned_patients) < 4:
            nurse.assign_patient(patient)
            return nurse
        print("No available nurse to assign.")
        return None

#This method books an appointment
    def book_appointment(self, patient_id, doctor_id, date, time):
            patient = self.patient.get(patient_id)
            doctor = self.doctor.get(doctor_id)
            if not patient or not doctor:
                print("Invalid patient or doctor ID.")
                return
            if not doctor.is_available(date, time):
                print("Doctor is not available at that time.")
                return
            nurse = self.assign_nurse_to_patient(patient)
            if nurse is None:
                print("No available nurse to assign.")
                return
            appointment = Appointment(patient, doctor, nurse, date, time)
            self.appointment[appointment.appointment_id] = appointment
            doctor.schedule.append((date, time))
            patient.book_appointment(appointment)
            appointment.confirmed()
            print(f"Doctor: {doctor.name}")
            print(f"Assigned nurse: {nurse.name}")

#This method cancels an appointment
    def cancel_appointment(self, appointment_id):
        appointment = self.appointment.get(appointment_id)
        if appointment:
            appointment.cancel()
        else:
            print("\nAppointment not found. Please redo cancellation\n")

#This method creates a new bill
    def generate_bill(self, appointment_id):
        appointment = self.appointment.get(appointment_id)
        if not appointment:
            print("Appointment not found.\n")
            return
        print("Consultation fee is $3000")
        add_service = input("Please enter additional service type: e.g, Labs/Blood test\n").strip().lower()
        if (any(char.isdigit() for char in add_service)
                or any(char in string.punctuation for char in add_service)
                or add_service == ""):
            print("Invalid service type. Your service type should only contain letters.")
            return
        try:
            cost = int(input("Please enter the amount for the service: $"))
            insurance = input("Do you have insurance? (yes/no): ").strip().lower()
            insurance_amt = 0
            if insurance == "yes":
                insurer = input("Enter the name of the insurance provider: e.g, Sagicor/Canopy")
                input("Enter policy number: ")
                insurance_amt = 2000
            consultation_fee = 3000
            sub_total = consultation_fee + cost
            total = sub_total - insurance_amt
            paid = int(input("Enter paid amount: $"))
            bal = total - paid
        except ValueError:
            print("Invalid number entered.")
            return

#The following displays a structured invoice
        print("\n\n-----------------------------------------INVOICE--------")
        print("Pilt Over Medical Hospital                                  ")
        print("Zaun District, Pilt Over                                    ")
        print("Runeterra, Japan                                            ")
        print("Telephone: +81 467-908-7763                                 ")
        print("------------------------------------------------------------")
        print(f"Patient: {appointment.patient.name}                        ")
        print(f"Doctor: {appointment.doctor.name}                          ")
        print(f"Appointment Date: {appointment.date}                       ")
        print("------------------------------------------------------------")
        print("Description            Cost                 Total           ")
        print("------------------------------------------------------------")
        print("Consultation Fee:      $3000                $3000           ")
        print(f"{add_service}:          ${cost}               ${cost}      ")
        print("------------------------------------------------------------")
        print(f"Subtotal:                                  ${sub_total}    ")
        print(f"Insurance coverage:            {insurer}   ${insurance_amt}")
        print("------------------------------------------------------------")
        print(f"Total Due:                                 ${total}        ")
        print(f"Paid:                                      ${paid}         ")
        print(f"Balance due:                               ${bal}          ")
        print("------------------------------------------------------------")


#Main loop for menu display and user input
def main():
    hospital = HospitalManagement()

#This part of the program has a while loop to display the menu to the user
    while True:
        print("\n\n           Pilt Over Medical Hospital           ")
        print("-----------------------------------------------------")
        print("A. Add new patient")
        print("B. Register a new doctor")
        print("C. Register a new nurse")
        print("D. Book an appointment")
        print("E. Cancel appointment")
        print("F. View doctor's schedule")
        print("G. View nurse's assigned patients")
        print("H. View patient profile")
        print("I. Create a new billing")
        print("J. Exit")

#This part of the program connects the user's choice to the functions
        choice = input("\nPlease select an option from the menu\n").strip().lower()

        #===========================>
        #Adding a new patient
        #===========================>
        if choice == "a":
            while True:
            #Name validation---------------------------->
                name = input("\nEnter patient name: ").strip()
                if (any(char.isdigit() for char in name)
                        or any(char in string.punctuation for char in name) or name == ""):
                    print("Invalid name. Your name should only contain letters.")
                else:
                    break
            #Age validation----------------------------->
            while True:
                age_str = input("Enter age: ").strip()
                if not age_str.isdigit():
                    print("Please enter a valid number")
                else:
                    age = int(age_str)
                    break
            if age > 125:
                print("\n***We’re only able to assist individuals from birth up to the age of 125..***\n")
                continue
            #Gender validation------------------------->
            while True:
                gender = input("Enter gender (M / F): ").strip().upper()
                if gender in ['M', 'F']:
                    break
                else:
                    print("Invalid gender. Try again")
            #Date of Birth validation------------------------->
            while True:
                    dateofbirth = input("Enter date of birth (YYYY-MM-DD): ").strip()
                    try:
                        valid_DoB = datetime.strptime(dateofbirth, "%Y-%m-%d")
                        birth_year = valid_DoB.year
                        current_year = datetime.now().year
                        age = current_year - birth_year
                        if age > 150 or age < 0:
                            print("Error. Please check your birth year.")
                        else:
                            break
                    except ValueError:
                        print("Invalid date format. Please enter as YYYY-MM-DD (e.g., 2000-05-10)")
            hospital.add_patient(name, age, gender,dateofbirth)

        #============================>
        #Adding a new doctor
        #============================>
        elif choice == "b":
            #Name validation---------------------------->
            while True:
                name = input("\nEnter doctor name: ").strip()
                if (any(char.isdigit() for char in name)
                        or any(char in string.punctuation for char in name) or name == ""):
                    print("Invalid name. Your name should only contain letters.")
                else:
                    break
            #Age validation---------------------------->
            while True:
                age_str = input("Enter age: ").strip()
                if not age_str.isdigit():
                    print("Please enter a valid number")
                else:
                    age = int(age_str)
                    break
            if age < 18 or age > 75:
                print("\n***This person is not eligible to work here. The acceptable age is 18-75 years old.***\n")
                continue
            #Gender validation------------------------->
            while True:
                gender = input("Enter gender (M / F): ").strip().upper()
                if gender in ['M', 'F']:
                    break
                else:
                    print("Invalid gender. Try again")
            #Date of Birth validation------------------->
            while True:
                   dateofbirth = input("Enter date of birth (YYYY-MM-DD): ").strip()
                   try:
                      valid_DoB = datetime.strptime(dateofbirth, "%Y-%m-%d")
                      birth_year = valid_DoB.year
                      current_year = datetime.now().year
                      age = current_year - birth_year
                      if age > 150 or age < 0:
                         print("Error. Please check your birth year.")
                      else:
                         break
                   except ValueError:
                       print("Invalid date format. Please enter as YYYY-MM-DD (e.g., 2000-05-10)")
            #Speciality validation--------------------->
            while True:
                speciality = input("Enter speciality: ").strip()
                if any(char.isdigit() for char in speciality) or speciality == "":
                    print("Error. Please enter a valid speciality")
                else:
                    break
            hospital.add_doctor(name, age, gender, dateofbirth, speciality)

            # =======================>
            # Adding a new nurse
            # =======================>
        elif choice == "c":
            # Name validation---------------------------->
            while True:
                name = input("\nEnter nurse name: ").strip()
                if (any(char.isdigit() for char in name)
                        or any(char in string.punctuation for char in name) or name == ""):
                    print("Invalid name. Your name should only contain letters.")
                else:
                    break
            # Age validation---------------------------->
            while True:
                age_str = input("Enter age: ").strip()
                if not age_str.isdigit():
                    print("Please enter a valid number")
                else:
                    age = int(age_str)
                    break
            if age < 18 or age > 75:
                print("\n***This person is not eligible to work here. The acceptable age is 18-75 years old.***\n")
                continue
            # Gender validation------------------------->
            while True:
                gender = input("Enter gender (M / F): ").strip().upper()
                if gender in ['M', 'F']:
                    break
                else:
                    print("Invalid gender. Try again")
            # Date of Birth validation------------------->
            while True:
                dateofbirth = input("Enter date of birth (YYYY-MM-DD): ").strip()
                try:
                    valid_DoB = datetime.strptime(dateofbirth, "%Y-%m-%d")
                    birth_year = valid_DoB.year
                    current_year = datetime.now().year
                    age = current_year - birth_year
                    if age > 150 or age < 0:
                        print("Error. Please check your birth year.")
                    else:
                        break
                except ValueError:
                    print("Invalid date format. Please enter as YYYY-MM-DD (e.g., 2000-05-10)")
            hospital.add_nurse(name, age, gender, dateofbirth)

        #==========================>
        #Booking an appointment
        #==========================>
        elif choice == "d":
            pID = input("\nEnter patient ID: ").strip()
            dID = input("Enter doctor ID: ").strip()
            #Date validation------------------------->
            while True:
                date = input("Appointment date (YYYY-MM-DD): ").strip()
                try:
                    datetime.strptime(date, "%Y-%m-%d")
                    break
                except ValueError:
                    print("Invalid date format. Please enter as YYYY-MM-DD (e.g., 2025-07-25)")
            #Time validation------------------------->
            while True:
                time = input("Enter appointment time (e.g., 2:30 PM): ").strip()
                try:
                    valid_time = datetime.strptime(time, "%I:%M %p")
                    break
                except ValueError:
                    print("Invalid time format. Please use HH:MM AM/PM.")
            hospital.book_appointment(pID, dID, date, time)

        #============================>
        #Cancelling an appointment
        #============================>
        elif choice == "e":
            apptID = input("\nEnter appointment ID: ").strip()
            hospital.cancel_appointment(apptID)

        #===============================================>
        #Viewing the doctor's scheduled appointments
        #===============================================>
        elif choice == "f":
            dID = input("\nEnter doctor's ID: ").strip()
            doctor = hospital.doctor.get(dID)
            if doctor:
                doctor.view_schedule()
            else:
                print("\nSchedule not found")

        # =======================================>
        # Viewing the nurse's assigned patients
        # =======================================>
        elif choice == "g":
            nID = input("Enter nurse's ID: ").strip()
            nurse = hospital.nurse.get(nID)
            if nurse:
                nurse.view_assigned_patients()
            else:
                print(" No assigned patients")

        #================================>
        #Viewing the patient's profile
        #================================>
        elif choice == "h":
            pProfile = input("\nEnter patient ID: ").strip()
            patient = hospital.patient.get(pProfile)
            if patient:
                patient.profile_display()
            else:
                print("\nPatient not found")

        #=====================================>
        #Generating a bill for the customer
        #=====================================>
        elif choice == "i":
            appointment_id = input("\nEnter appointment ID: ").strip()
            hospital.generate_bill(appointment_id)

        #====================>
        #Exit the program
        #====================>
        elif choice == "j":
            print("Login terminated successfully.")
            break
        else:
            print("Invalid option please try again.")

#Runs the code
if __name__ == "__main__":
    main()