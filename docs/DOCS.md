# Project: Grow

Convenience wrapper for obtaining view count metadata through Wikipedia's APIs.

## 📁 Collection: Top

### End-point: Get Top Monthly Views

Get the top viewed articles by month.

#### Get Top Monthly Views Method: POST

>```bash
>http://127.0.0.1:8000/top
>```

#### Get Top Monthly Views Body (**raw**)

```json
{
    "project": "en.wikipedia",
    "year": "2022",
    "month": "12",
    "day": "04",
    "granularity": "monthly",
    "access": "all-access"
}
```

#### Get Top Monthly Views Response

```json
{
   "items":[
      {
         "project":"en.wikipedia",
         "access":"all-access",
         "year":"2022",
         "month":"12",
         "day":"04",
         "articles":[
            {
               "article":"Main_Page",
               "views":5247331,
               "rank":1
            },
            "..."
         ]
      }
   ]
}
```

---

### End-point: Get Top Weekly Views

Get the top viewed articles by week.

#### Get Top Weekly Views Method: POST

>```bash
>http://127.0.0.1:8000/top
>```

#### Get Top Weekly Views Body (**raw**)

```json
{
    "project": "en.wikipedia",
    "year": "2022",
    "month": "12",
    "day": "04",
    "granularity": "weekly",
    "access": "all-access"
}
```

#### Get Top Weekly Views Response

```json
{
    "items": [
        {
            "project": "en.wikipedia",
            "access": "all-access",
            "year": "2022",
            "month": "12",
            "day": "04",
            "articles": [
                {
                    "article": "Main_Page",
                    "views": 34649181,
                    "rank": 1
                },
                ...
            ]
        }
    ]
}
```

---

### End-point: Get Top Daily Views

Get the top viewed articles by day.

#### Get Top Daily Views Method: POST

>```bash
>http://127.0.0.1:8000/top
>```

#### Get Top Daily Views Body (**raw**)

```json
{
    "project": "en.wikipedia",
    "year": "2022",
    "month": "12",
    "day": "04",
    "granularity": "daily",
    "access": "all-access"
}
```

#### Get Top Daily Views Response

```json
{
    "items": [
        {
            "project": "en.wikipedia",
            "access": "all-access",
            "year": "2022",
            "month": "12",
            "day": "04",
            "articles": [
                {
                    "article": "Main_Page",
                    "views": 34649181,
                    "rank": 1
                },
                ...
            ]
        }
    ]
}
```

---

## 📁 Collection: Top by Article

### End-point: Get Views Between Dates (Week)

#### Top by Article Method: POST

>```bash
>http://127.0.0.1:8000/top/Paris
>```

#### Top by Article Body (**raw**)

```json
{
    "project": "en.wikipedia",
    "start_date": "20221218",
    "end_date": "20221224",
    "agent": "all-agent",
    "access": "all-access"
}
```

#### Top by Article Response

```json
{
    "items": [
        {
            "project": "en.wikipedia",
            "article": "Paris",
            "granularity": "daily",
            "timestamp": "2022121800",
            "access": "all-access",
            "agent": "all-agents",
            "views": 25229
        },
        ...
    ],
    "total_views": 91935,
    "max_view": {
        "project": "en.wikipedia",
        "article": "Paris",
        "granularity": "daily",
        "timestamp": "2022121800",
        "access": "all-access",
        "agent": "all-agents",
        "views": 25229
    }
}
```

---

### End-point: Get Views Between Dates (Month)

#### Get Views Between Dates (Month) Method: POST

>```bash
>http://127.0.0.1:8000/top/Paris
>```

#### Get Views Between Dates (Month) Body (**raw**)

```json
{
    "project": "en.wikipedia",
    "start_date": "20221201",
    "end_date": "20221231",
    "agent": "all-agent",
    "access": "all-access"
}
```

#### Get Views Between Dates (Month) Response

```json
{
    "items": [
        {
            "project": "en.wikipedia",
            "article": "Paris",
            "granularity": "daily",
            "timestamp": "2022120100",
            "access": "all-access",
            "agent": "all-agents",
            "views": 18175
        },
        ...
    ],
    "total_views": 414670,
    "max_view": {
        "project": "en.wikipedia",
        "article": "Paris",
        "granularity": "daily",
        "timestamp": "2022121800",
        "access": "all-access",
        "agent": "all-agents",
        "views": 25229
    }
}
```

---
