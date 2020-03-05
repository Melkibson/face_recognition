import cv2
import numpy as np

if __name__ == '__main__':

    # ルックアップテーブルを作成するため変数の定義
    solarization_const = 2 * np.pi / 255

    # ルックアップテーブルの生成
    """
    array([[0],
           [0],
           [0],
           [0],
           [0],
           [0],
           [0],
        ・・・・・・・・
           [0], dtype='uint8')
    のようなリストが生成される。
    """
    look_up_table = np.ones((256, 1), dtype = 'uint8' ) * 0

    for i in range(256):

        look_up_table[i][0] = np.abs(np.sin(i * solarization_const)) * 100

    # 画像の読み込み
    img_src = cv2.imread("training-data/dorian/dorian.jpg", 1)

    # ソラリゼーション後の出力
    img_sola = cv2.LUT(img_src, look_up_table)

    # 表示
    cv2.imshow("Show SOLARIZATION Image", img_sola)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
