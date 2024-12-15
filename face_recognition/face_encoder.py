import torch
from facenet_pytorch import InceptionResnetV1

class FaceEncoder:
    def __init__(self):
        self.resnet = InceptionResnetV1(pretrained='vggface2').eval()

    def encode_face(self, face_image):
        face_tensor = torch.from_numpy(face_image).unsqueeze(0).permute(0, 3, 1, 2).float()
        face_encoding = self.resnet(face_tensor)
        return face_encoding

    def compare_faces(self, test_encoding, known_encodings, threshold=0.4):
        results = []

        for encoding in known_encodings:
            distance = torch.norm(test_encoding - encoding, 2)
            is_match = distance < threshold
            results.append((is_match.item(),distance.item()))

        return results,