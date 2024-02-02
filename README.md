![](https://img.shields.io/badge/STATUS-NOT%20CURRENTLY%20MAINTAINED-red.svg?longCache=true&style=flat)

# Important Notice
This public repository is read-only and no longer maintained. For the latest sample code repositories, visit the [SAP Samples](https://github.com/SAP-samples) organization.

# Conversational AI Rest API Example using SAP Translation Hub

[![REUSE status](https://api.reuse.software/badge/github.com/SAP-samples/conversational-ai-rest-api-example)](https://api.reuse.software/info/github.com/SAP-samples/conversational-ai-rest-api-example)

## Description
This project is a concrete scenario showing a broad spectrum of REST APIs use cases for Conversational AI. <br/>
This is an example use of SAP Conversational AI and SAP Translation Hub REST APIs in order to help translating a dataset on the CAI platform. <br/>
It translates a JSON dataset (in a CAI-format or exported from the platform) and import the translations back to the CAI platform. It also has the possibility to download the translated CAI-format JSON dataset.<br/>

DISCLAIMER: This tool is only an example of how CAI APIs can be used. We don’t use it in production and we’re not planning any updates, nor support on this topic. It should not be used to process any personal data.

## Requirements 

* Python environment setup completed
* Available account on [SAP Conversational AI](https://cai.tools.sap/) (at least a trial account) and an already created chatbot
* Available account on [SAP Translation Hub](https://www.sapstore.com/solutions/40076/SAP-Translation-Hub)

## Download and Installation

The first step is to clone the repository.<br/>
Then it's necessary to install some Python libraries :
```
> pip install -r requirements.txt
```

### Usage

Basic generation :
```
> python3 ./bin/translate.py -p PATH -a API -s SOURCE_LANG -t TARGET_LANG -user USER_SLUG -bot BOT_SLUG -version VERSION_SLUG -devtoken DEV_TOKEN -botid BOT_ID -botsecret BOT_SECRET -id CLIENT_ID -secret CLIENT_SECRET
```
**-p** or **--path** is the path of the original JSON dataset <br/>
**-a** or **--api** is the translation API you’d like to use for the translations (optional, `saptranslationhub` by default) <br/>
**-s** or **--sourcelang** is the source language of the original dataset<br/>
**-t** or **--targetlang** is the target language of the translations<br/>
**-user** or **--userslug** is the user slug of the bot owner in the CAI platform<br/>
**-bot** or **--botslug** is the bot slug of the bot in the CAI platform <br/>
**-version** or **--versionslug** is the version slug of the bot in the CAI platform <br/>
**-devtoken** or **--developertoken** is the developer token corresponding to the bot in the CAI platform <br/>
**-botid** or **--botclientid** is the bot's OAuth client id for authentication of Designtime APIs on the CAI platform <br/>
**-botsecret** or **--botclientsecret** is the bot's OAuth client secret for authentication of Designtime APIs on the CAI platform <br/>
**-id** or **--clientid** is the client id of the SAP Translation Hub account <br/>
**-secret** or **--clientsecret** is the client secret of the SAP Translation Hub account

You can check which translation is supported on [SAP Translation Hub](https://help.sap.com/viewer/9f73362817cd48339dd8a6acba160f7f/Cloud/en-US/6fc2e5ab04a94da4a0c3d0740a9bb2ff.html) <br/>

If the input JSON dataset is already in a CAI-format, you can add the argument **-format** (or **--formatfile**) by specifying the format `cai`, otherwise the input dataset is in an exported-from-platform format by default.
```
> python3 ./bin/translate.py -p PATH -a API -s SOURCE_LANG -t TARGET_LANG -user USER_SLUG -bot BOT_SLUG -version VERSION_SLUG -devtoken DEV_TOKEN -botid BOT_ID -botsecret BOT_SECRET -id CLIENT_ID -secret CLIENT_SECRET -format cai
```

If you’d like to save the translated JSON dataset on a CAI-format, you can add the argument **-save**.
```
> python3 ./bin/translate.py -p PATH -a API -s SOURCE_LANG -t TARGET_LANG -user USER_SLUG -bot BOT_SLUG -version VERSION_SLUG -devtoken DEV_TOKEN -botid BOT_ID -botsecret BOT_SECRET -id CLIENT_ID -secret CLIENT_SECRET -save
```

### Input and output formats
Example of a JSON dataset exported from the CAI platform, as input :
```
{
    "version": 5,
    "datasets": [
        {
            "slug": null,
            "created_at": "2021-02-10T12:56:00.351Z",
            "updated_at": "2021-07-22T15:24:01.917Z",
            "strictness": 50,
            "type": 0,
            "classifier": 4,
            "recognizer": 0,
            "manual_training": true,
            "big_bot": false,
            "bot_id": "09034b4d-5962-4290-b8b1-a960268e6ae1",
            "version_id": "2374ca87-4541-4751-bc94-9afc6d919bb4",
            "is_forking": false,
            "resolve_pronouns": false,
            "resolve_descriptions": false,
            "last_data_update_at": "{\"en\": \"2021-07-22T08:52:23.677Z\", \"fr\": \"2021-07-22T15:24:01.917Z\"}",
            "language": "en",
            "restricted_entity_strictness": 90,
            "free_entity_strictness": 0,
            "is_generating": false,
            "sharenet": 0
        }
    ],
    "intents": [
        {
            "slug": "greetings",
            "created_at": "2021-02-10T12:56:05.547Z",
            "updated_at": "2021-07-01T13:09:12.057Z",
            "description": "Says hello",
            "name": "greetings",
            "rating": 0,
            "dataset_id": 0,
            "is_activated": true,
            "position": 2,
            "is_forking": false,
            "strictness": null
        }
    ],
    "entities": [
        {
            "dataset_id": 0,
            "entity_id": null,
            "is_open": true,
            "is_activated": true,
            "slug": "pronoun",
            "created_at": "2021-02-10T12:56:00.377Z",
            "updated_at": "2021-02-10T12:56:00.377Z",
            "strictness": null,
            "enrichment_strictness": 95,
            "is_custom": false,
            "color": "#cffff4",
            "name": "PRONOUN",
            "is_forking": false,
            "webhook_id": null,
            "gold_enrichment_from": null,
            "enrichment_type": null,
            "enrichment_webhook_id": null,
            "locked": true,
            "type": 0,
            "regex_pattern": null,
            "regex_flags": null
        }
    ],
    "expressions": [
        {
            "intent_id": 0,
            "source": "hey vous",
            "created_at": "2021-07-21T12:32:28.648Z",
            "updated_at": "2021-07-21T12:32:28.648Z",
            "tokens": "[{\"pos\":\"PROPN\",\"word\":\"hey\",\"space\":true},{\"pos\":\"PRON\",\"word\":\"vous\",\"space\":false,\"entity_id\":21}]",
            "language": "fr"
        }
    ],
    "synonyms": [],
    "validation_files": [],
    "enrichment_pair_keys": [],
    "default_enrichment_values": [],
    "enrichment_groups": [],
    "enrichment_pair_values": [],
    "entity_group_values": []
```

Example of CAI-format JSON dataset as input:
``` 
{
    "id": "cc8b9d33-c7f1-4565-aa89-c16d10fc6754",
    "language": "en",
    "dataset_language": "en",
    "classifier": "embedding_surface_logistic_regression",
    "sharenet": "community",
    "recognizer": "conditional_random_fields",
    "strictness": 50,
    "restricted_entity_strictness": 90,
    "free_entity_strictness": 0,
    "intents": [
        {
            "id": "49e6f952-3f69-4265-bf4e-8a2fdcc7b1e9",
            "name": "greetings",
            "description": "Says hello",
            "strictness": null,
            "expressions": [
                {
                    "id": "62921442-7c76-4e2f-976f-4d6e5acfb892",
                    "source": "Hey you",
                    "compiled": "Hey PRONOUN",
                    "tokens": [
                        {
                            "word": "Hey",
                            "space": true,
                            "pos": "INTJ",
                            "entity": null
                        },
                        {
                            "word": "you",
                            "space": false,
                            "pos": "PRON",
                            "entity": {
                                "name": "PRONOUN",
                                "type": "gold",
                                "is_custom": false
                            }
                        }
                    ]
                }
            ]
        }
    ],
    "gazettes": [
        {
            "id": "ba21c702-a02a-4193-9f5f-bf74830039ed",
            "name": "PRONOUN",
            "slug": "pronoun",
            "locked": true,
            "type": "gold",
            "is_open": false,
            "strictness": null,
            "enrichment_strictness": 95,
            "synonyms": [],
            "enrichments": {
                "enrichment_pair_keys": {},
                "enrichment_groups": []
            },
            "regex_pattern": null,
            "regex_flags": null
        }
    ],
    "exported_at": "2021-07-21T09:21:38.040Z"
}
```
The script will first translate the synonyms then the expressions.
Once the loading bar has finished, the translated expressions are supposed to appeared in the platform in the desired language, as well as the translated synonyms. The expressions are also supposed to be annotated with gold, free and restricted entities.<br/>


If you chose to save the translated CAI-format JSON dataset, a file will be created on the same path as your original dataset, and it will look like this :

```
{
    "id": "cc8b9d33-c7f1-4565-aa89-c16d10fc6754",
    "language": "fr",
    "dataset_language": "en",
    "classifier": "embedding_surface_logistic_regression",
    "sharenet": "community",
    "recognizer": "conditional_random_fields",
    "strictness": 50,
    "restricted_entity_strictness": 90,
    "free_entity_strictness": 0,
    "intents": [
        {
            "id": "49e6f952-3f69-4265-bf4e-8a2fdcc7b1e9",
            "name": "greetings",
            "description": "Says hello",
            "strictness": null,
            "expressions": [
                {
                    "id": "62921442-7c76-4e2f-976f-4d6e5acfb892",
                    "source": "hey vous",
                    "compiled": "hey PRONOUN",
                    "tokens": [
                        {
                            "word": "hey",
                            "space": true,
                            "pos": "PROPN",
                            "entity": null
                        },
                        {
                            "word": "vous",
                            "space": false,
                            "pos": "PRON",
                            "entity": {
                                "name": "PRONOUN",
                                "type": "gold",
                                "is_custom": false
                            }
                        }
                    ]
                }
            ]
        }
    ],
    "gazettes": [
        {
            "id": "ba21c702-a02a-4193-9f5f-bf74830039ed",
            "name": "PRONOUN",
            "slug": "pronoun",
            "locked": true,
            "type": "gold",
            "is_open": false,
            "strictness": null,
            "enrichment_strictness": 95,
            "synonyms": [],
            "enrichments": {
                "enrichment_pair_keys": {},
                "enrichment_groups": []
            },
            "regex_pattern": null,
            "regex_flags": null
        }
    ],
    "exported_at": "2021-07-21T09:21:38.040Z"
}
```

## Known Issues
The sample is provided only as an example use. Currently, there are no known issues for the sample project.

## How to obtain support
The sample is provided only as an example use. There is no guarantee that raised issues will be answered or addressed in future releases.

[Create an issue](https://github.com/SAP-samples/<repository-name>/issues) in this repository if you find a bug or have questions about the content.
 
For additional support, [ask a question in SAP Community](https://answers.sap.com/questions/ask.html).



## Contributing
If you wish to contribute code, offer fixes or improvements, please send a pull request. Due to legal reasons, contributors will be asked to accept a DCO when they create the first pull request to this project. This happens in an automated fashion during the submission process. SAP uses [the standard DCO text of the Linux Foundation](https://developercertificate.org/).


## License
Copyright (c) 2021 SAP SE or an SAP affiliate company. All rights reserved. This project is licensed under the Apache Software License, version 2.0 except as noted otherwise in the [LICENSE](LICENSES/Apache-2.0.txt) file.

