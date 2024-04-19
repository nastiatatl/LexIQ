# LexIQ
Final project for COSI 217b NLP Systems

wordhoard retrieves synonyms but it is very slow. it does use a caching system so the synonyms are stored there until the session is over. 

possible solutions:
- another library/api (nltk?)
- create a cache file with most common words and their synonyms (might take forever, won't cover everything anyway)
- combine synonym retrieval and quiz generation, ask gpt to do both (given examples)

as of now, you can input words or upload a csv file and the app will display their synonyms

TODO:
- quiz generation - sort of done, needs testing with actual quizzes
- synonyms caching/database
- quiz caching/database
- quiz page - done
  - scoring - done, displays the user's choice and whether it was correct or not
- testing - started, not yet pushed
- requirements.txt (already started)
- CSS styling - mostly done, CSS file needs major clean-up