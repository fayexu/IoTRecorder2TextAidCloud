##### Test partial functionality
### 1. publish audio 
```shell
python publisher.py myiotthingcchw ../data/have_a_nice_day.m4a publish speechsensing
```

### 2. subscriber a topic from pub
```shell
python subscriber.py myiotthingcchw receive speech-to-transcribe
```

### 3. upload audio file to s3
```shell
python upload.py
```

### 4. transcribe audio file
```shell
python transcribe.py
```

### 5. create QLDB
1. Use AWS console to create a [QLDB](https://ap-southeast-1.console.aws.amazon.com/qldb/home?region=ap-southeast-1#getting-started "Title")
2. [Access QLDB](https://docs.aws.amazon.com/qldb/latest/developerguide/accessing.html "Title") 
3. QLDB [endpoints](https://docs.aws.amazon.com/general/latest/gr/qldb.html "Title")

### 6. save transcript to QLDB
```shell
python test_connection.py
```
```shell
python qldb-quick-start.py
```
