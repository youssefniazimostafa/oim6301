import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    Data = [
    	{
    		"name": "Babson AI",
    		"vendor": "customendpoint",
    		"apiKey": "${input:chat.lm.secret.2abb96f4}",
    		"apiType": "messages",
    		"models": [
    			{
    				"id": "claude-sonnet-5",
    				"name": "Sonnet 5 (Babson)",
    				"url": "https://ca-litellm-mint-eus2.orangeflower-5d81efa8.eastus2.azurecontainerapps.io/v1/messages",
    				"toolCalling": True,
    				"vision": True,
    				"maxInputTokens": 200000,
    				"maxOutputTokens": 32000
    			}
    		]
    	}
    ]
    Data
    return (Data,)


@app.cell
def _(Data):
    Data[0]["name"]
    return


@app.cell
def _(Data):
    Data[0]["models"][0]["name"]
    return


if __name__ == "__main__":
    app.run()
