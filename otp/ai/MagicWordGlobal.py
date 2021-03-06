import traceback


class MagicError(Exception):
    pass


def ensureAccess(access, msg='Insufficient access'):
    if spellbook.getInvokerAccess() < access:
        raise MagicError(msg)


class Spellbook:
    """
    The Spellbook manages the list of all Magic Words that have been registered
    anywhere in the system. When the MagicWordManager(AI) wants to process a
    Magic Word, it is passed off to the Spellbook, which performs the operation.

    To add Magic Words to the Spellbook, use the @magicWord() decorator.
    """

    def __init__(self):
        self.words = {}

        self.currentInvoker = None
        self.currentTarget = None

    def addWord(self, word):
        self.words[word.name.lower()] = word  # lets make this stuff case insensitive

    def process(self, invoker, target, incantation):
        self.currentInvoker = invoker
        self.currentTarget = target
        word, args = (incantation.split(' ', 1) + [''])[:2]

        try:
            return self.doWord(word, args)
        except MagicError as e:
            return e.message
        except Exception:
            return traceback.format_exc()
        finally:
            self.currentInvoker = None
            self.currentTarget = None

    def doWord(self, wordName, args):
        wordName = wordName.lower()
        word = self.words.get(wordName)

        if not word:
            if process == 'ai':
                for key in self.words:
                    if self.words.get(key).access <= self.getInvokerAccess():
                        if wordName in key:
                            return 'Did you mean %s' % self.words.get(key).name
            if not word:
                return

        ensureAccess(word.access)
        if self.getTarget() and self.getTarget() != self.getInvoker():
            if self.getInvokerAccess() <= self.getTarget().getAdminAccess():
                raise MagicError('Target must have lower access')

        result = word.run(args)
        if result is not None:
            return str(result)

    def getInvoker(self):
        return self.currentInvoker

    def getTarget(self):
        return self.currentTarget

    def getInvokerAccess(self):
        if not self.currentInvoker:
            return 0
        return self.currentInvoker.getAdminAccess()

    def getTargets(self, word):
        if word == "":
            return
        word = self.words.get(word.split()[0].lower())
        if word is None:
            return []

        return word.targets


spellbook = Spellbook()


# CATEGORIES
class MagicWordCategory:
    def __init__(self, name, defaultAccess=600):
        self.name = name
        self.defaultAccess = defaultAccess


CATEGORY_UNKNOWN = MagicWordCategory('Unknown')
CATEGORY_USER = MagicWordCategory('Community manager', defaultAccess=100)
CATEGORY_COMMUNITY_MANAGER = MagicWordCategory('Community manager', defaultAccess=200)
CATEGORY_MODERATOR = MagicWordCategory('Moderator', defaultAccess=300)
CATEGORY_CREATIVE = MagicWordCategory('Creative', defaultAccess=400)
CATEGORY_PROGRAMMER = MagicWordCategory('Programmer', defaultAccess=500)
CATEGORY_ADMINISTRATOR = MagicWordCategory('Administrator', defaultAccess=600)
CATEGORY_SYSTEM_ADMINISTRATOR = MagicWordCategory('System administrator', defaultAccess=700)

MINIMUM_MAGICWORD_ACCESS = CATEGORY_COMMUNITY_MANAGER.defaultAccess


class MagicWord:
    def __init__(self, name, func, types, targets, access, doc):
        self.name = name
        self.func = func
        self.types = types
        self.targets = targets
        self.access = access
        self.doc = doc

    def parseArgs(self, string):
        maxArgs = self.func.func_code.co_argcount
        minArgs = maxArgs - (len(self.func.func_defaults) if self.func.func_defaults else 0)

        args = string.split(None, maxArgs-1)[:maxArgs]
        if len(args) < minArgs:
            raise MagicError('Magic word %s requires at least %d arguments' % (self.name, minArgs))

        output = []
        for i, (type, arg) in enumerate(zip(self.types, args)):
            try:
                targ = type(arg)
            except (TypeError, ValueError):
                raise MagicError('Argument %d of magic word %s must be %s' % (i, self.name, type.__name__))

            output.append(targ)

        return output

    def run(self, rawArgs):
        args = self.parseArgs(rawArgs)
        return self.func(*args)


class MagicWordDecorator:
    """
    This class manages Magic Word decoration. It is aliased as magicWord, so that
    the @magicWord(...) construct instantiates this class and has the resulting
    object process the Magic Word's construction.
    """

    def __init__(self, name=None, types=[str], targets=['DistributedToonAI'], access=None, category=CATEGORY_UNKNOWN):
        self.name = name
        self.types = types
        self.category = category
        self.targets = targets

        if access is not None:
            self.access = access
        else:
            self.access = self.category.defaultAccess

    def __call__(self, mw):
        # This is the actual decoration routine. We add the function 'mw' as a
        # Magic Word to the Spellbook, using the attributes specified at construction
        # time.

        name = self.name
        if name is None:
            name = mw.func_name

        word = MagicWord(name, mw, self.types, self.targets, self.access, mw.__doc__)
        spellbook.addWord(word)

        return mw

magicWord = MagicWordDecorator
