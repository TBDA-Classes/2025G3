# Extraction / Data analysis  Overview
This branch is for the extraction and analyst team to be able to extract the data with a code that does not affect the backend/frontend. 
This so the team can analyse and see different data which will be important for the decision of data for the different KPIs and such.
## What this module does
- Exploring data in the database
- Make queeries for different variables and datasets to explore them
- Analyse different data and there frequenzies
## What has been done
- The extraction group have checked the database and looked through all the ID.s that are interesting for the client to be seen. These have later been translated from the unit ids to variable ids. An exceldocument was after this created so the backend and frontend teams could use the right IDs. Discussions in the the whole team has also unfolded where talks about which parameters to use. 
- Code for extraction with different queries have been developed and used for the extraction.

## 24/11-25
- A code for extraction of system status as on/off has been developed where the querie counts all the variables that are active every hour during set dates. By looking at when the variables are not active, we can see when the machine is on or off. This is done with the following querie that looks at all the variables in variable_log_float instead of specific IDs.

- q = text("""
    SELECT
        DATE(to_timestamp(date/1000)) AS day,
        EXTRACT(HOUR FROM to_timestamp(date/1000)) AS hour,
        COUNT(*) AS log_count
    FROM public.variable_log_float
    WHERE date BETWEEN :start_ms AND :end_ms
    GROUP BY day, hour
    ORDER BY day, hour;
""")

This is the result for a five day period in january in 2015.

<img width="2866" height="985" alt="Screenshot 2025-11-27 162236" src="https://github.com/user-attachments/assets/6ee18e92-20a4-4877-bd87-ee422db93647" />

<img width="2781" height="1401" alt="Screenshot 2025-11-27 162216" src="https://github.com/user-attachments/assets/cf7d71f2-da2e-47cb-8d33-b39b5e59e6e4" />

The full code can be seen in the extraction folder under system_status.py 
## Code Reference
