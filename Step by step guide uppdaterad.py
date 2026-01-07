/* Step by step guide för att få fram sample datan till en fil som demo:

1. Sök upp följande i claude chatten:

download_bigquery_data.py

-------
2. 
*/
Kör följande script i terminal:

cd C:\Users\Patri\Documents\ai-analytics-demo

3.

ladda ner google cloud bigquery, kör:

pip install google-cloud-bigquery db-dtypes pandas pyarrow

4.

Testa Google cloud, kör:

gcloud --version

5.
Logga in och connecta till GCP, kör:

gcloud auth application-default login

-------

6. 
Ladda ner datan, kör:

python download_bigquery_data.py

-------------
7. 
# Lista filer
dir *.csv


---------------------------------------------

COMPLETE STREAMLIT DEMO BUILD GUIDE

cd C:\Users\Patri\Documents\ai-analytics-demo

8.
Install Streamlit, kör:

pip install streamlit plotly

9. Spara ner "demo_app.py"


10. Run Your Demo Locally, kör:

streamlit run demo_app.py

pip install streamlit plotly
streamlit run demo_app.py


Info:

-- Demo_app URL:

http://localhost:8504/

🎉 Your app is live at:
https://ai-analytics-demo-xyz123.streamlit.app

-- Kolla även hur jag kan lägga till detta öppet på Github eller ge access vid behov

- Hur kan jag dela streamlit sidan vid behov, kanske bättre att använda ett annat verktyg:
https://share.streamlit.io/deploy


Kolla hur jag kan förbättra modellen så att Claude läser direkt från tabellen istället och kan svara på datan.
Snygga till grafer. Behövs så många tabeller och grafer verkligen eller kan dessa läggas till längre fram.


Sök på i Claude:

Steg 1.3: Gör Demo "Sales-Ready" (Dag 6-7)

When I asked the following question:

Can you create the entire python code and steps for Googles 4 datasets instead of random created datasets:


# Set your name (shows in commits)
git config --global user.name "olofssonpatric"

# Set your email (use same as GitHub)
git config --global user.email "olofssonpatric@gmail.com"


git init