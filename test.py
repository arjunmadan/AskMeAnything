import wolframalpha

app_id = "TRR8TK-VHV99K9UE8"
client = wolframalpha.Client(app_id)

res = client.query('temperature in Charlottesville, VA on February 28, 2015')

print(next(res.results).text)

