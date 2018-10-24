import mlab
import csv
from models.service import User, Song, Place, Video, Book
mlab.connect()
admin = User.objects(username="admin", password="admin").first()
admin_id = str(admin["id"])
# new_place = Place(
#                 happy = 2,
#                 name = "Naturaw Phan Chu Trinh",
#                 describe = "Food",
#                 link = "55 Phan Chu Trinh, Hoàn Kiếm, Hà Nội, Vietnam",
#                 # link_img = "http://i3.ytimg.com/vi/3hOpP3brwtY/maxresdefault.jpg",
#                 user_id =admin_id)
# new_place.save()

# with open('place.csv', 'r') as f:
#   reader = csv.reader(f)
#   your_list = list(reader)
#
# # link_img = []
# # for i in range(1,101):
# #     link_img.append(your_list[i][4])
# #
# happy = []
# for i in range(1,68):
#     happy.append(your_list[i][0])
# #
# name = []
# for i in range(1,101):
#     name.append(your_list[i][1])
# #
# describe = []
# for i in range(1,101):
#     describe.append(your_list[i][2])
#
# link = []
# for i in range(1,68):
#     link.append(your_list[i][3])
# #
# # link = []
# # for i in range(1,101):
# #     link.append(your_list[i][3])
# #
# for i in range(67):
#     new_place = Place(
#                     happy = happy[i],
#                     name = name[i],
#                     describe = describe[i],
#                     link = link[i],
#
#                     user_id =admin_id)
#     new_place.save()
#
all_books = Song.objects()
j = 0
for i in all_books:
    j += 1
    print(j,i['name'])
