# PaintPalWebsite

Course project for CSCI 8836, Intro to Software Engineering

This is a project that I am working on for my current graduate software engineering course. I am proud of it because I am the sole contributer to this project, despite the idea for this project not being my own. I must admit that while I do not find the central premise of the website to be too interesting, this challenge has allowed me to incorporate new functionalities that I have not been able to use before. Furthermore, I was able to implement the PyPy just in time (JIT) compiler in place of the typical Python interpreter to allow for reduced server-side latency. Finally, if you pull the main branch down and run it locally, you may find that I incorporated a fun easter egg that may be found at localhost:8000/easterEgg/. I used this to illustrate the speed benefits associated with dynamic programming techniques. By using dynamic programming, I was able to reduce the time complexity associated with calculating the Fibonacci Sequence from O(2^n) down to O(n). - Samuel Schneider


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
