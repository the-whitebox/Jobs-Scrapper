# import openai

# openai.api_key='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'
# #print(openai.Model.list())


# input_text = """ About the job Senior Staff Nurse Cardiac - Full-Time Location: The Harley Street Clinic, London Salary: Competitive plus 9% shift enhancements + Private Medical + Pension and many more benefits.Job Overview We have an exciting opportunity for a cardiac senior staff nurse to join our cardiac nursing team The Harley Street Clinic in London. Our leading consultant cardiologists, cardiac surgeons and specialist nurses carry out pioneering work, aided by highly advanced medical technology.You will work within our Cardiac Centre which offers a range of treatment options, from screening and diagnosis of common conditions such as coronary artery disease, to minimally invasive procedures such as inserting stents and pacemakers, as well as offering highly specialised surgeries such as minimal access mitral valve repair.\n\nThe ward involves Interventional Cardiology, Cardiothoracic surgery, vascular and robotics as well as cardiac/medical conditions that require continuous monitoring and treatment.You will already be registered with the Nursing and Midwifery Council, with cardiac surgical specialist skills. Your training should include postgraduate qualifications and a minimum of ILS, ideally ALS. You will also have extensive senior level knowledge and will have a minimum of 2 years experience in working in your current setting. Youll be accountable for leading, motivating, educating and supervising the nursing and multidisciplinary team.Skills And Experience NMC Registered Nurse (RN Adult)Relevant courses in Cardiology/Cardiothoracic\nExperience of working with acute/chronically ill patients in a cardiac setting"


# """

# response = openai.Edit.create(
#   model="text-davinci-edit-001",
#   input = input_text,
#   instruction="find the keywords from given text ",
#   temperature = 0.8
# )

# for choice in response['choices']:
#     print(choice['text'])
import os
import openai

openai.api_key = "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"
q="I am ENT SPecialist "
response = openai.Completion.create(
model="text-davinci-003",
prompt=f"This is an intelligent conversation between human and AI jobs search\n\nQ: {q} \nA:",
temperature=0,
max_tokens=100,
top_p=1,
frequency_penalty=0.0,
presence_penalty=0.0,
stop=["\n"])
for response in response['choices']:
    print(response['text'])
