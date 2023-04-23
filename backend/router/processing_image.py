from fastapi import APIRouter, File, HTTPException
import cv2
import numpy as np
from utils import utilities
from schemas.result import ProcessingImage
from base64 import b64decode
from model.result import Result
from model.score import Score
from model.user import User
from utils.db import transaction

router = APIRouter()


@router.post('/base64_img')
async def processing(file: ProcessingImage):
    for img in file.image:
        with open("imageToSave.png", "wb") as fh:
            fh.write(b64decode(img.split(',').pop()))
        processing_image(
            'imageToSave.png', file.is_result, img.split(',').pop(), file.subject, file.is_overwrite, file.grading_again
        )


@router.post('/')
async def create_file(file: bytes = File()):

    # with open("16.jpg", 'rb') as fp:
    #     img = fp.read()
    img = np.frombuffer(file, np.uint8)
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)

    img = cv2.resize(img, (660, 600))
    # im_cv = cv2.imread(im_path)
    img2 = img.copy()
    img3 = img.copy()
    # print(img)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # img_gray = cv2.resize(img_gray, (350, 550))

    blur = cv2.GaussianBlur(img_gray, (5, 5), 0)
    img_canny = cv2.Canny(blur, 10, 100)

    contours, hierarchy = cv2.findContours(img_canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(img.copy(), contours, -1, (0, 255, 0), 2)
    rect_con = utilities.rect_contour(contours)

    bigContours = utilities.getCornerPoints(rect_con[0])
    mssvContours = utilities.getCornerPoints(rect_con[1])
    ma_De_Contours = utilities.getCornerPoints(rect_con[2])

    result = {}

    img_info = {
        'result': {
            'contours': utilities.getCornerPoints(rect_con[0]),
            'position': [[0, 0], [660, 0], [0, 1000], [660, 1000]],
            'size': {
                'img': (660, 1000), 'ans': (25, 11), 'resize': (330, 500)
            },
            'img': img.copy(),
            'img_cut': None
        },
        'student': {
            'contours': utilities.getCornerPoints(rect_con[1]),
            'position': [[0, 0], [700, 0], [0, 700], [700, 700]],
            'size': {
                'img': (700, 700), 'ans': (10, 7), 'resize': (150, 250)
            },
            'img': img.copy(),
            'img_cut': None
        },
        'code': {
            'contours': utilities.getCornerPoints(rect_con[2]),
            'position': [[0, 0], [660, 0], [0, 600], [660, 600]],
            'size': {
                'img': (660, 600), 'ans': (10, 3), 'resize': (150, 250)
            },
            'img': img.copy(),
            'img_cut': None
        }
    }

    if bigContours.size != 0 and mssvContours.size != 0 and ma_De_Contours.size != 0:
        for area, value in img_info.items():
            # if area != 'code': continue
            cv2.drawContours(value['img'], value['contours'], -1, (0, 255, 0), 10)
            pt1 = np.float32(utilities.reoder(value['contours']))
            pt2 = np.float32(value['position'])
            matrix = cv2.getPerspectiveTransform(pt1, pt2)
            value['img_cut'] = cv2.warpPerspective(img_gray, matrix, value['size']['img'])
            img_result_color = cv2.warpPerspective(img2, matrix, value['size']['img'])
            img_dra = np.zeros_like(img_result_color)

            img_thersh = cv2.threshold(value['img_cut'], 100, 255, cv2.THRESH_BINARY_INV)[1]
            img_thersh_resize = cv2.resize(img_thersh, value['size']['resize'])
            cv2.imwrite(f"img_thersh{area}.jpg", img_thersh_resize)

            fill = ""

            if area == 'result':
                # crop image
                cell_width = value['size']['resize'][0] / value['size']['ans'][1]
                img_left = img_thersh_resize[0:value['size']['resize'][1], 0: int(cell_width*4)]
                img_right = img_thersh_resize[
                    0:value['size']['resize'][1],
                    int(value['size']['resize'][0] - int(cell_width*4)): value['size']['resize'][0]
                ]
                for col in [img_left, img_right]:
                    matrix = utilities.split_boxes(col, value['size']['ans'][0], 4)
                    fill += find_filled_cell(matrix, [25, 4], True)
                img_dra = utilities.showAns(img_dra, [1, 3, 2, 1], [1, 1, 0, 1], [1, 3, 1, 1], 25, 11)

                matrix_result = cv2.getPerspectiveTransform(pt2, pt1)
                img_result = cv2.warpPerspective(img_dra, matrix_result, (660, 600))
                #
                # cv2.putText(img3, "cai gi", (350, 100), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 2)
                img3 = cv2.addWeighted(img3, 0.7, img_result, 1, 0)
                #
                imgtl = cv2.resize(img3, (550, 500))
                cv2.imwrite(f"img_dra{area}.jpg", imgtl)

            else:
                matrix = utilities.split_boxes(img_thersh, value['size']['ans'][0], value['size']['ans'][1])
                fill = find_filled_cell(matrix, value['size']['ans'], False)

            result[area] = fill

    return result


def processing_image(path, is_result, image, subject, is_overwrite=False, grading_again=False):
    img = cv2.resize(cv2.imread(path), (660, 600))
    # im_cv = cv2.imread(im_path)
    img2 = img.copy()
    img3 = img.copy()
    # print(img)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # img_gray = cv2.resize(img_gray, (350, 550))

    blur = cv2.GaussianBlur(img_gray, (5, 5), 0)
    img_canny = cv2.Canny(blur, 10, 100)

    contours, hierarchy = cv2.findContours(img_canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(img.copy(), contours, -1, (0, 255, 0), 2)
    rect_con = utilities.rect_contour(contours)

    bigContours = utilities.getCornerPoints(rect_con[0])
    mssvContours = utilities.getCornerPoints(rect_con[1])
    ma_De_Contours = utilities.getCornerPoints(rect_con[2])

    result = {}

    img_info = {
        'result': {
            'contours': utilities.getCornerPoints(rect_con[0]),
            'position': [[0, 0], [660, 0], [0, 1000], [660, 1000]],
            'size': {
                'img': (660, 1000), 'ans': (25, 11), 'resize': (330, 500)
            },
            'img': img.copy(),
            'img_cut': None
        },
        'student': {
            'contours': utilities.getCornerPoints(rect_con[1]),
            'position': [[0, 0], [700, 0], [0, 700], [700, 700]],
            'size': {
                'img': (700, 700), 'ans': (10, 7), 'resize': (150, 250)
            },
            'img': img.copy(),
            'img_cut': None
        },
        'code': {
            'contours': utilities.getCornerPoints(rect_con[2]),
            'position': [[0, 0], [660, 0], [0, 600], [660, 600]],
            'size': {
                'img': (660, 600), 'ans': (10, 3), 'resize': (150, 250)
            },
            'img': img.copy(),
            'img_cut': None
        }
    }

    if bigContours.size != 0 and mssvContours.size != 0 and ma_De_Contours.size != 0:
        for area, value in img_info.items():
            # if area != 'code': continue
            cv2.drawContours(value['img'], value['contours'], -1, (0, 255, 0), 10)
            pt1 = np.float32(utilities.reoder(value['contours']))
            pt2 = np.float32(value['position'])
            matrix = cv2.getPerspectiveTransform(pt1, pt2)
            value['img_cut'] = cv2.warpPerspective(img_gray, matrix, value['size']['img'])
            img_result_color = cv2.warpPerspective(img2, matrix, value['size']['img'])
            img_dra = np.zeros_like(img_result_color)

            img_thersh = cv2.threshold(value['img_cut'], 100, 255, cv2.THRESH_BINARY_INV)[1]
            img_thersh_resize = cv2.resize(img_thersh, value['size']['resize'])
            cv2.imwrite(f"img_thersh{area}.jpg", img_thersh_resize)

            fill = ""

            if area == 'result':
                # crop image
                cell_width = value['size']['resize'][0] / value['size']['ans'][1]
                img_left = img_thersh_resize[0:value['size']['resize'][1], 0: int(cell_width * 4)]
                img_right = img_thersh_resize[
                            0:value['size']['resize'][1],
                            int(value['size']['resize'][0] - int(cell_width * 4)): value['size']['resize'][0]
                            ]
                for col in [img_left, img_right]:
                    matrix = utilities.split_boxes(col, value['size']['ans'][0], 4)
                    fill += find_filled_cell(matrix, [25, 4], True)
                img_dra = utilities.showAns(img_dra, [1, 3, 2, 1], [1, 1, 0, 1], [1, 3, 1, 1], 25, 11)

                matrix_result = cv2.getPerspectiveTransform(pt2, pt1)
                img_result = cv2.warpPerspective(img_dra, matrix_result, (660, 600))
                #
                # cv2.putText(img3, "cai gi", (350, 100), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 2)
                img3 = cv2.addWeighted(img3, 0.7, img_result, 1, 0)
                #
                imgtl = cv2.resize(img3, (550, 500))
                cv2.imwrite(f"img_dra{area}.jpg", imgtl)

            else:
                matrix = utilities.split_boxes(img_thersh, value['size']['ans'][0], value['size']['ans'][1])
                fill = find_filled_cell(matrix, value['size']['ans'], False)

            result[area] = fill

        result['result'] = list(map(lambda x: int(x), list(result['result'])))
        # feature of teacher: create result
        if is_result:
            # check duplicate
            result_exists = Result.get_or_none(code=result['code'], subject=subject)

            if result_exists:
                if is_overwrite:
                    Result.update_one(
                        result_exists.id,
                        image,
                        {'code': result['code'], 'subject': subject, 'result': result['result']}
                    )

                    if grading_again:
                        Score.update_by_subject_and_code(subject, result['code'])

                else:
                    raise HTTPException(400, 'result already exists')
            else:
                Result.create(image, **{'code': result['code'], 'subject': subject, 'result': result['result']})

        # save score of student
        else:
            # check is exists
            student = User.get_or_none(code=result['student'])
            if subject in student.subject_ids:
                score_exists = Score.get_or_none(code=result['code'], subject=subject, student=student.id)
                if score_exists:
                    Score.update_one(score_exists.id, image, **{
                        'code': result['code'], 'subject': subject, 'filled_cell': result['result'], 'student': student.id
                    })
                else:
                    Score.create(image, **{
                        'code': result['code'], 'subject': subject, 'filled_cell': result['result'], 'student': result['student']
                    })
            else:
                raise HTTPException(400, 'student not in this class')
    # return result


def find_filled_cell(matrix, size_ans, is_result):
    fill = ''
    index_c = 0
    index_r = 0
    count_non_zero = np.zeros(size_ans)

    for image2 in matrix:
        # if area == 'code':
        #     print(cv2.countNonZero(image2), 124)
        count_non_zero[index_r][index_c] = cv2.countNonZero(image2)
        index_c += 1
        if index_c == size_ans[1]:
            index_r += 1
            index_c = 0
    if not is_result:
        count_non_zero = np.transpose(count_non_zero)

    for arr in count_non_zero:
        if list(filter(lambda x: x > 100, arr)):
            fill += str(np.where(arr == np.amax(arr))[0][0])

    return fill
