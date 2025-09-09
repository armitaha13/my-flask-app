CREATE DATABASE dental_clinic;
USE dental_clinic;
CREATE TABLE services (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);
CREATE TABLE appointments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_name VARCHAR(100) NOT NULL,
    patient_phone VARCHAR(11) NOT NULL, -- چون صفر اول اگر INT باشه پاک میشه
    patient_nationalCode VARCHAR (10) NOT NULL,
    appointment_date VARCHAR(20) NOT NULL, -- چون تاریخ رو به شمسی وارد میکنیم نه میلادی و خود دیتا بیس اوتومات تاریخ را میلادی میکند پس به جای DATE از VERCHAR استفاده میکنیم
    appointment_time TIME NOT NULL,
    descriptions varchar(100),
    refrences boolean,
    service_id INT NOT NULL,
    FOREIGN KEY (service_id) REFERENCES services(id)
);
INSERT INTO services (name) VALUES
("عصب کشی"),
("ترمیم دندان"),
("جرم گیری"),
("جراحی لثه"),
("کشیدن دندان"),
("کشیدن دندان عقل"),
("کامپوزیت"),
("لمینیت"),
("ارتودنسی"),
("چک آپ"),
("رادیولوژی"),
("ایمپلنت");
INSERT INTO appointments (patient_name, patient_phone, patient_nationalCode, appointment_date, appointment_time, service_id) VALUES
('Maryam Hosseini', '09121111111', '1234567890' , '1404-05-26', '10:00:00',1 ),  
('Hossein Ahmadi', '09122222222', '1234567890' , '1404-05-27', '11:00:00',2 ),  
('Parisa Nazari', '09123333333', '1234567890' , '1404-06-05', '09:30:00',3 ),  
('Amir Tavakoli', '09124444444', '1234567890' , '1404-06-23', '14:00:00', 4),  
('Neda Jafari', '09125555555', '1234567890' , '1404-06-29', '13:00:00', 5 ),
('Tina Naghikhani','09039738895', '1234567890' , '1404-07-02', '14:30:00', 6 ),  
('Armita Ghiasvand', '09120002233', '1234567890' , '1404-07-15', '10:30:00', 7 ),
('Saba Bagheri', '09101234455', '1234567890' , '1404-07-24', '17:45:00', 8 ),  
('Melika Ebadi', '09039993366', '1234567890' , '1404-08-04', '12:15:00', 9 ),  
('Bita Moghadasi', '09123457789', '1234567890' , '1404-08-16', '13:30:00', 10),  
('Hosein Baghaei', '09030004476', '1234567890' , '1404-09-12', '16:30:00', 11),  
('Mojgan Babaei', '09121993662', '1234567890' , '1404-09-23', '18:00:00', 12);
SELECT * FROM services;
SELECT * FROM appointments;


