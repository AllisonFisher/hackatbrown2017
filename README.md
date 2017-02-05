# Diversity Scorecard

---


## Our Motivation
We want to fight unconscious bias by alerting people to diversity trends in the online media they consume on a daily basis.

## Technologies Used

*	Microsoft Azure (Virtual Machine)
*	Microsoft Cognitive Services (Face API)
*	LAMP Server

## Our Pipeline
We use the Face API from Microsoft's Cognitive Services to track people across frames and determine the gender of each person. We also estimate a racial category (using the categories for the United States Office of Management and Budget 1997 guidelines) by comparing each face to a sample of faces representing each racial category, and reporting which category had the highest confidence matches.

## Challenges

* Microsoft's APIs doesn't provide a way to track specific people from frame to frame, so we implemented this functionality ourselves.
* For obvious reasons, there are no existing commercial computer vision applications that support racial identification. Our approach is skewed by the set of images we selected to be "representative" of each racial group, and also in the idea that racial classification is something that can be done on the basis of facial appearance alone. We're aware that self-identification is the preferred method for collecting data on racial and ethnic categories, because of large differences between how people classify themselves and how they report others usually classify them.
* The API we used limited us to reporting a binary gender (Male/Female).

## Extensions and Future Work

* Use the Microsoft Cognitive Services Speech and Language APIs to implement an automated Bechdel test for videos (determining the number of conversations that two female characters have about something other than a man/boy).
* Package our analyzer into a Chrome extension that offers a pop-up diversity report for all images and videos on a webpage.
* Enhance our racial diversity metrics, through machine learning and user annotation.

