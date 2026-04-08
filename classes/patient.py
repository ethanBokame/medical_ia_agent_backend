class Patient:

    def __init__(self, age, gender, weight, size):
      self.age = age
      self.gender = gender
      self.weight = weight
      self.size = size

    def getPatientData(self):
      return {
        "age": self.age,
        "weight": self.weight,
        "gender": self.gender,
        "size": self.size
      }