# Securtiy
    1) implement asymmetric cryptosystem for api endpoints.

# Perfomance
    1) migrate to IPC instead of Redis?


# logic
    1) if confidence high, keep in array for more time.
    2) if confidence is high and is at parking space, give extra time before removing.
    3) dont allow to upload near MBH LH and major buildings
    4) add a set to busentry that tracks the current riders. Should clear the set if inside parking area.
    5) add timestamp ordering. dont allow old uploads to modify data. (should help with slow packet upload)

# app side
    1) check if user in LH or MBH or any building. If inside building dont send data.
    2) check speed and send it regardless of accuray
    3) implemnet swipe down reload.
    4) dont allow to upload location if inside buildings

# Notes
    - Used ray casting algorithm to check if inside polygon
    - 

