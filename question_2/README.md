# Question 2 Text Sanitizer

Problems: Please write a "text sanitizer" application in any OOP languages (Python 3 preferred)
    - receive CLI arguments "source" & "target"
    - read a text file from "source" as an input data
    - sanitize the input text (receive string and return string)
        - lowercase the input
        - replace "tab" with "____"
    - generate simple statistic
        - count number of occurrence of each alphabet.
    - print output(both sanitized text & statistic) to console.

Description: This application is used for mocking and test this problem solution. There are five functions in this application:
    - text_sanitizing: return string in lowercase and replace "tab" with "____"
    - text_statistics: return the statistics (count an alphabet) of string
    - write_local: save output file to local folder.
    - write_gcs: save output file to Google Cloud Storage.
    - process_file: executing the whole process