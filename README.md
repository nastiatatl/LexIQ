# cosi_217b_final_project
Final project for COSI 217b NLP Systems

wordhoard retrieves synonyms but it is very slow. it does use a caching system so the synonyms are stored there until the session is over. 

possible solutions:
- another library/api (nltk?)
- create a cache file with most common words and their synonyms (might take forever, won't cover everything anyway)
- ???

as of now, you can input words and the app will display their synonyms

TODO:
- quiz generation - sort of done, needs testing with actual quizzes
- synonyms caching/database
- quiz caching/database
- quiz page - done
  - scoring - partially done, need to fix styling
- testing
- requirements.txt (already started)
- formatting - started experimenting