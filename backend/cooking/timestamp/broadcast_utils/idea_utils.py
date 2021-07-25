import os
import time
import json


def checkTagStringLength(tag_string):
    """get initial input from user (string with tags) and check if it is not too long"""
    return len(tag_string) > 50


def get_json_tags(tag_string):
    """ take a tag string with one or more separated by comma's  tags,
    get rid of "" items (line 28) and convert it to a list in json format
    """
    # print("util func get_json_tags for a tag stirng to work with", tag_string, "len", len(tag_string))
    tag_list = [item.strip(",.:;'*)/(!") for item in tag_string.split(",") if len(item) != 0]
    # print("after strip and ect got tag_list", tag_list, "length", len(tag_list))
    if len(tag_list) != 0:
        if tag_list[-1] == " ":
            print("found , at the end of the list")
            tag_list = tag_list[:-1]
    clear_tag_list = [item for item in tag_list if len(item) > 0]

    # print("see result in form of list", clear_tag_list)
    # print("type of result is", type(clear_tag_list))  # list ['foo','bar']
    return json.dumps(clear_tag_list)


def upload_img(instance, filepath):
    """make path to uploaded file (avatar) and adjust file name if needed 
    note: used user id instead of instance (because it doesn't have it yet)
    """
    # TODO: check for spaces or other awkward characters in file name
    filename = os.path.basename(filepath)         # 'abababa.jpeg'
    name, ext = os.path.splitext(filename)         # tuple ('abababa', '.jpeg')
    if len(name) > 5:
        name = name[:5]
    new_file_name = name + str(time.time()) + ext
    # timestamp = timezone.now().strftime("%Y-%m-%d")
    # if isinstance(instance,cls)
    klass = (instance.__class__.__name__).lower()
    if klass == 'idea':
        user_folder = f'idea_{instance.author.id}'
        # new_file_name = name + instance.slug+ext
        # return os.path.join('ideapot', new_file_name)
        return os.path.join('ideapot', user_folder, new_file_name)
    elif klass == 'profile':
        # new_file_name = name + instance.unid+ext
        user_folder = f'profile_{instance.user.id}'
        return os.path.join('avatar', user_folder, new_file_name)


def make_img_name_shortcut(name):
    # ideapot/idea_1/chess1619044791.952363.JPG
    raw = name.split("/")[-1]
    extention = raw.split('.')[-1]
    head_list = raw.split('.')[:-1]
    head = "".join(head_list)
    if len(head) > 10:
        head = head[:10]
    return f"{head}.{extention}"