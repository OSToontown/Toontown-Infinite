from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal


class GlobalOtpObject(DistributedObjectGlobal):
    notify = directNotify.newCategory('GlobalOtpObject')
