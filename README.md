# CodaLab competition for the CoNLL 2019 Shard Task on Cross-Framework Meaning Representation Parsing #

This is a competition bundle for the [CodaLab competition](https://competitions.codalab.org/) used in the [CoNLL 2019 on Cross-Framework Meaning Representation Parsing](http://mrp.nlpl.eu/).

The Makefile creates a ZIP file that includes all the YAML and HTML files in the competition directory, as well as the zipped-up scoring program and reference data.
To do this automatically, you can run:

    make competition.zip

That ZIP file can then be used to [create a new competition at CodaLab](https://competitions.codalab.org/competitions/create).

Once the competition has uploaded successfully, try uploading a submission.
  You can generate a sample submission at the command line by running
  
    make submission.zip

  Then in the CodaLab competition:

  - Click on "Participate". Click on "Submit / View Results".
  - Enter a suitable description for each submission in the text box provided.
  - Click on the "Submit" button to upload the file.
  - This should execute the evaluation script on the submission and store the results.
  - You can monitor the progress on the "Submit / View Results" page by clicking the "+" beside your submission and then clicking on "Refresh status".
  - Your submission should move from "Submitted" to "Running" to "Finished".
  - When it is "Finished", explore various files generated on running the evaluation script. For example, text sent to STDOUT will be available in "View scoring output log".
  - Click on "Results" to see the leaderboard.
