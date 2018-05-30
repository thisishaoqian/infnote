import faker from 'faker'

var TopicData = [
    {title: 'Why choose to go to the moon', author: 'Vergil', replies: 12324215, last: 'Hao Qian'},
    {title: 'We choose to build this!', author: 'Hao Qian', replies: 45234561, last: 'Vergil'},
    {title: 'Something that so cool!', author: 'Anonymous', replies: 12324215, last: 'Anonymous'},
    {title: 'Bitcoin Core 16.0 Released', author: 'Hao Qian', replies: 12324215, last: 'Hao Qian'},
    {title: 'How to find a good programmer to do custom development in my exchange ?', author: 'David', replies: 12324215, last: 'Jack'},
    {title: 'How does margin trade settlement work?', author: 'Vergil', replies: 12324215, last: 'Haoqian'},
]

for (var i = 0; i < 100; i++) {
    TopicData.push({
        title: faker.lorem.sentence(),
        author: faker.name.findName(),
        replies: Math.round(Math.random() * 10000000),
        last: faker.name.findName(),
    })
}

export default TopicData
