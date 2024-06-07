# To-do and other notes

## Hey Spotify
When Superbird detects "Hey Spotify", it starts streaming microphone audio to the phone in ogg format in .5 second chunks. Currently, connector just writes the audio to a .ogg file.

Need to implement transcript response from the Spotify app. Looks like this:\
In this example, I said "testing".
```
{
   'session_id':'2024-06-01T08_47_34.893Z.ogg',
   'utterance_id':'fe83181a-8c50-4880-b6a9-e60f8b1470f8',
   'message':'AsrResponse',
   'asr':{
      'transcript':'testing',
      'isFinal':True,
      'isEndOfSpeech':True,
      'score':0.8085283041000366
   }
}
```
This is sent as an EVENT to `com.spotify.superbird.voice.session_updates`\
`session_id` is the .ogg filename in microphone data packets\
`transcript` can be a partial or final transcript\
When speech-to-text is done, `isFinal` and `isEndOfSpeech` get set to True and Superbird displays the transcript.\
I'm currently not 100% how search results are added to the home screen, but it's likely with the message below.

When Spotify starts speaking, it sends `{'state': 'STARTED'}` as an EVENT to `com.spotify.superbird.tts.state`.

When results are ready, Spotify sends following message as an EVENT to `com.spotify.superbird.voice.session_updates`
```
{
   'session_id':'2024-06-01T09_04_33.963Z.ogg',
   'utterance_id':'3d4e3dc9-e0aa-42c4-9b84-e5203fb17c05',
   'message':'NluResponse',
   'nlu':{
      'body':[
         {
            'text':{
               'title':'52 Hearts',
               'subtitle':'Bao The Whale'
            },
            'images':{
               'main':{
                  'uri':'spotify:image:ab67616d00001e02d9508aea9edad0274d1b37bd'
               }
            },
            'target':{
               'uri':'spotify:track:7MGLRs9ZsPiOHSY3zMIjhm'
            },
            'custom':{
               'albumReleaseDate':'2020-11-08',
               'popularity':41
            }
         },
         {
            'text':{
               'title':'rare animal',
               'subtitle':'glass beach'
            },
            'images':{
               'main':{
                  'uri':'spotify:image:ab67616d00001e0237295d61bcd9fc7fa2fe33c9'
               }
            },
            'target':{
               'uri':'spotify:track:0KCbWi4LF8rpY8U93T1Mwu'
            },
            'custom':{
               'albumReleaseDate':'2024-01-19',
               'popularity':40
            }
         },
         {
            'text':{
               'title':'Silhouette (feat. Milk Talk)',
               'subtitle':'Moe Shop, Milk Talk'
            },
            'images':{
               'main':{
                  'uri':'spotify:image:ab67616d00001e02f43d59dd385e10e9d393a89c'
               }
            },
            'target':{
               'uri':'spotify:track:3geVGPVgAH9SNk0YBG6Y3E'
            },
            'custom':{
               'albumReleaseDate':'2023-09-22',
               'popularity':34
            }
         }
         {
            'text':{
               'title':'classic j dies and goes to hell part 1',
               'subtitle':'glass beach'
            },
            'images':{
               'main':{
                  'uri':'spotify:image:ab67616d00001e02382ddf73e0132cecf399c718'
               }
            },
            'target':{
               'uri':'spotify:track:3ezuOjWuTirncJITAb8ahf'
            },
            'custom':{
               'albumReleaseDate':'2019-05-18',
               'popularity':45
            }
         },
         {
            'text':{
               'title':'Revive',
               'subtitle':'LIONE'
            },
            'images':{
               'main':{
                  'uri':'spotify:image:ab67616d00001e0295970b868b8c32728ff95fd4'
               }
            },
            'target':{
               'uri':'spotify:track:4Bb53fsDAero14LpAbsmft'
            },
            'custom':{
               'albumReleaseDate':'2019-10-24',
               'popularity':40
            }
         },
         {
            'text':{
               'title':'Fantasy',
               'subtitle':'Moe Shop, MONICO'
            },
            'images':{
               'main':{
                  'uri':'spotify:image:ab67616d00001e025fcd8144ff007592c8018cd7'
               }
            },
            'target':{
               'uri':'spotify:track:1awjNR40wYscCumpP4zFVM'
            },
            'custom':{
               'albumReleaseDate':'2018-03-15',
               'popularity':33
            }
         },
         {
            'text':{
               'title':'Citrus Love',
               'subtitle':'Bao The Whale, Overspace'
            },
            'images':{
               'main':{
                  'uri':'spotify:image:ab67616d00001e027827895c48fd8598a3507494'
               }
            },
            'target':{
               'uri':'spotify:track:3RiYi67LMqBpopK1b1D0fb'
            },
            'custom':{
               'albumReleaseDate':'2023-04-15',
               'popularity':44
            }
         },
         {
            'text':{
               'title':'You Can Give Spaghetti to a Rat',
               'subtitle':'Classic J'
            },
            'images':{
               'main':{
                  'uri':'spotify:image:ab67616d00001e02e770277875c6eebda14019bd'
               }
            },
            'target':{
               'uri':'spotify:track:1h63tRjR186VhlXehT6P44'
            },
            'custom':{
               'albumReleaseDate':'2020-03-20',
               'popularity':11
            }
         },
         {
            'text':{
               'title':'gemini',
               'subtitle':"Snail's House"
            },
            'images':{
               'main':{
                  'uri':'spotify:image:ab67616d00001e02330cfe664d55a588e96e27f2'
               }
            },
            'target':{
               'uri':'spotify:track:3CHpLb1IXma99y3brtXfco'
            },
            'custom':{
               'albumReleaseDate':'2023-02-03',
               'popularity':29
            }
         }
      ],
      'custom':{
         'ttsPrompt':'<speak xml:lang="en-US">Sure, 52 Hearts <break time="100ms"/> plus other search results.</speak>',
         'content_id':'spotify:space_item:superbird:superbird-voice',
         'spotify_active':True,
         'ttsUrl': 'Omitted just in case. Spotify does TTS on their servers using ReadSpeaker and this url points to the TTS mp3',
         'query':'testing',
         'action':'SHOW_TRACK',
         'intent':'SHOW',
         'connect_action_taken':False
      }
   }
}
```
After it's done speaking, it sends `{'state': 'FINISHED'}` as an event to `com.spotify.superbird.voice.session_updates`

Sometimes the app will send other EVENTs like this: (In this example, I said 'save this song')
```
{
   'session_id':'2024-06-07T05_32_09.977Z.ogg',
   'utterance_id':'3366b181-3147-46d9-ab6b-bbf87ac1fe1c',
   'message':'NluResponse',
   'nlu':{
      'body':[
         
      ],
      'custom':{
         'slots':{
            'requestedEntityType':[
               'song'
            ]
         },
         'ttsPrompt':'<speak xml:lang="en-US">Saved</speak>',
         'content_id':'spotify:space_item:superbird:superbird-voice',
         'spotify_active':True,
         'ttsUrl':'Omitted just in case. Spotify does TTS on their servers using ReadSpeaker and this url points to the TTS mp3',
         'query':'save this song',
         'action':'SAVE_TO_COLLECTION_TRACK',
         'intent':'ADD_TO_COLLECTION',
         'connect_action_taken':False
      }
   }
}
```
Intent and action handler code can be found here: [https://github.com/Merlin04/superbird-webapp/tree/modded/component/VoiceConfirmation](https://github.com/Merlin04/superbird-webapp/tree/modded/component/VoiceConfirmation)

## Potential future features
- Phone calls - I thought phone calls were handled via some wierd iOS specific bluetooth thing but it looks like they're still handled by the Spotify app
https://github.com/Merlin04/superbird-webapp/blob/5781976ec7fb56aceeedc7c4bcb7c83b70067636/store/AndroidPhoneCallStore.ts#L41
