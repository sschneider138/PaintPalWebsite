# PaintPalWebsite

Course project for CSCI 8836, Intro to Software Engineering

Welcome to PaintPal!
PaintPal is a web application that allows you to input the dimensions to your room, 
and calculate the estimate for the amount of paint you will need to cover that space.
Users can save their estimations through their account for later use, and share them with 
others. Users can input their room by specifying the lengths and positions of walls, as well as
other possible architectural elements such as soffits or diagonal walls. Click "Start Visualizing"
on the home page to begin designing a room layout. Use "Login" or "Register" on the top
navigation bar to manage your account for saved estimations.

# Release Notes
-6/22/2023
-Added home page, about page, hello world page (temporary)
-Added login and register pages, with associated account functionality
-Added profile page for registered users

-7/15/2023
-Added backend authentication validation for user accounts
-Added added volume calculation for one wall
-Added functionality for metric or US standard units, whichever user prefers
-Added docker virtial postgres db found in docker-compose.yml file


-8/14/2023
-Added backend image processing to highlight largest planar surface
-Added calculations to extract real-world distances from image
-Added upload and cleanup processes for image upload
-Added upload page for image
-Added dimension importing from image for wall height and length