### 9. publish audio 
```shell
python publisher.py myiotthingcchw ./data/have_a_nice_day.m4a publish speechsensing
```

### 10. subscriber a topic from pub
```shell
python subscriber.py myiotthingcchw receive speech-to-transcribe
```

### 11. upload audio file to s3
```shell
python upload.py <bucket id> <path to audil file>
```

### 12. transcribe audio file
```shell
python transcribe.py <bucket id> <region> <audio name> <job name> 
```

### 13. create QLDB
1. Use AWS console to create a [QLDB](https://ap-southeast-1.console.aws.amazon.com/qldb/home?region=ap-southeast-1#getting-started "Title")
2. [Access QLDB](https://docs.aws.amazon.com/qldb/latest/developerguide/accessing.html "Title") 
3. QLDB [endpoints](https://docs.aws.amazon.com/general/latest/gr/qldb.html "Title")

### 14. save transcript to QLDB

