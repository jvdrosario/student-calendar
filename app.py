from flask import Flask, request, jsonify
from parserPython import extract_text_from_pdf
from extractdata import extract_data_from_txt
import os
import tempfile
import asyncio

app = Flask(__name__)


def run_async_task(coroutine):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(coroutine)


@app.route('/extract_events', methods=['POST'])
async def extract_events():
    try:
        # Ensure a PDF file is sent
        file = request.files.get('pdf')
        if not file:
            return jsonify({"error": "No PDF file uploaded"}), 400

        # Save the uploaded file to a temporary location
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        file.save(temp_file.name)

        # Step 1: Convert PDF to text
        text = extract_text_from_pdf(temp_file.name)
        temp_file.close()
        os.remove(temp_file.name)

        if not text:
            return jsonify({"error": "Failed to extract text from PDF"}), 400
        temp_text_file = tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w", encoding="utf-8")

        temp_text_file.write(text)
        temp_text_file.close()
        # print(text)
        df = await extract_data_from_txt(temp_text_file.name)
        os.remove(temp_text_file.name)

        # Step 2: Extract events from text
        # events_df = asyncio.run(extract_data_from_txt(text))  # Note: 'text' should be the file path here
        # events = events_df.to_dict(orient="records")  # Convert DataFrame to list of dicts
        events = df.to_json(orient="records")

        # Clean up the temporary file
        # Return the extracted events in JSON format

        # return jsonify({"events": events})
        print(events)
        return events

    except Exception as e:
        print(e)
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)
