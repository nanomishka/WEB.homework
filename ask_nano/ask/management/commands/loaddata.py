from django.core.management.base import BaseCommand
from optparse import make_option

from ask.models import Profile, Question, Answer, Tags, Quest_tags
from django.contrib.auth.models import User

from faker.frandom import random
from faker.lorem import sentence, sentences
from mixer.fakers import get_username, get_email
from pprint import pformat

from django.db.models import Min, Max

class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option('--users',
            action='store',
            dest='users',
            default=0,
        ),
        make_option('--questions',
            action='store',
            dest='questions',
            default=0,
        ),
        make_option('--answers',
            action='store',
            dest='answers',
            default=0,
        ),
        make_option('--tags',
            action='store',
            dest='tags',
            default=0,
        ),
        make_option('--quest_tag',
            action='store',
            dest='quest_tag',
            default=0,
        ),
    )

    def handle(self, *args, **options):
        names = {}
        while(len(names.keys())<int(options['users'])):
            names[get_username(length=30)]=1

        for name in names.keys():
            u = User.objects.create(username=name+str(random.randint(0,100)), email=get_email())
            p = Profile.objects.create(user_id=u.id, rating = random.randint(0,20))

        p_min = Profile.objects.all().aggregate(Min('id'))['id__min']
        p_max = Profile.objects.all().aggregate(Max('id'))['id__max']
        q_min = Question.objects.all().aggregate(Min('id'))['id__min']
        q_max = Question.objects.all().aggregate(Max('id'))['id__max']
        t_min = Tags.objects.all().aggregate(Min('id'))['id__min']
        t_max = Tags.objects.all().aggregate(Max('id'))['id__max']

        f = open('/var/lib/mysql/askdb/data.csv', 'w')
        

        for i in range(0, int(options['questions'])):
            title =sentence()[0:random.randint(40,80)].replace('.','?')
            text = sentence()[0:random.randint(20,40)].replace('.','?')
            author_id = str(random.randint(p_min,p_max))
            sl = '\\'
            f.write(sl+sl+'\t'+title+'\t'+text+'\t'+sl+sl+'\t'+author_id+'\n')
            #LOAD DATA INFILE 'data.csv' INTO TABLE ask_question;

        for i in range(0, int(options['answers'])):
            text = sentence()[0:random.randint(20,40)].replace('.','?')
            author_id = str(random.randint(p_min,p_max))
            quest_id = str(random.randint(q_min,q_max))
            is_right = str(random.randint(0,1))
            sl = '\\'
            f.write(sl+sl+'\t'+text+'\t'+sl+sl+'\t'+is_right+'\t'+author_id+'\t'+quest_id+'\n')
            #LOAD DATA INFILE 'data.csv' INTO TABLE ask_answer;

        for i in range(0, int(options['tags'])):
            tag = sentence()
            tag = tag[0:tag.find(' ')]
            sl = '\\'
            f.write(sl+sl+'\t'+tag+'\n')
            #LOAD DATA INFILE 'data.csv' INTO TABLE ask_tag;

        for i in range(0, int(options['quest_tag'])):
            quest_id = str(random.randint(q_min,q_max))
            tag_id = str(random.randint(t_min,t_max))
            sl = '\\'
            f.write(sl+sl+'\t'+quest_id+'\t'+tag_id+'\n')
            #LOAD DATA INFILE 'data.csv' INTO TABLE ask_quest_tag;

        f.close()

        print(p_max,p_min)