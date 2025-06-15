# Country To Code Converter

Developed a Python script that efficiently maps country names to their respective ISO country codes using advanced string matching techniques. The script leverages the difflib library for fuzzy matching, allowing it to handle partial matches, alternative spellings, and directional abbreviations (e.g., "korea n" for "Korea (North)"). The program loads country data from a CSV file, performs optimized searches, and returns the most relevant match based on similarity ratios. This tool is particularly useful for data normalization tasks in applications requiring accurate country code mappings. The script also includes performance metrics to measure search efficiency.

### Activate Environment
```bash
python -m venv env-name
.\env-name\Scripts\Activate
```

## Project Setup

```bash
pip install -r requirements.txt

# Run my app using command
streamlit run main.py
