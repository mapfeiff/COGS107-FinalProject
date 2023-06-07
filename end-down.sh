#Ensure the username and email are anonymous to protect subject identity
git config user.name "Anonymous"
git config user.email "anon@user.com"

#Add the confirm the changes that were made to the csv file
git add --all

#Commit the changes, saving the data under an anonymous user
git commit -m "Test Complete; Data Uploaded"

#Anonymously push the changes to the repository
git push