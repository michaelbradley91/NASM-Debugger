from PyQt5.QtCore import QRegularExpression, Qt, QRegularExpressionMatchIterator, QRegularExpressionMatch, QRegExp
from PyQt5.QtGui import QSyntaxHighlighter, QTextDocument, QTextCharFormat, QFont, QColor

from widgets.syntax_highlighters.highlighting_rule import HighlightingRule

# noinspection SpellCheckingInspection
KEYWORD_PATTERNS = ["aaa", "aad", "aam", "aas", "adc", "add", "and", "call", "cbw", "clc", "cld", "cli", "cmc", "cmp",
                    "cmpsb",
                    "cmpsw", "cwd", "daa", "das", "dec", "div", "esc", "hlt", "idiv", "imul", "in", "inc", "int",
                    "into",
                    "iret", "ja", "jae", "jb", "jbe", "jc", "jcxz", "je", "jg", "jge", "jl", "jle", "jna", "jnae",
                    "jnb",
                    "jnbe", "jnc", "jne", "jng", "jnge", "jnl", "jnle", "jno", "jnp", "jns", "jnz", "jo", "jp", "jpe",
                    "jpo",
                    "js", "jz", "jmp", "lahf", "lds", "lea", "les", "lock", "lodsb", "lodsw", "loop", "loope", "loopne",
                    "loopnz", "loopz", "mov", "movsb", "movsw", "mul", "neg", "nop", "not", "or", "out", "pop", "popf",
                    "push",
                    "pushf", "rcl", "rcr", "rep", "repe", "repne", "repnz", "repz", "ret", "retn", "retf", "rol", "ror",
                    "sahf",
                    "sal", "sar", "sbb", "scasb", "scasw", "shl", "shr", "stc", "std", "sti", "stosb", "stosw", "sub",
                    "test",
                    "wait", "xchg", "xlat", "xor", "bound", "enter", "ins", "leave", "outs", "popa", "pusha", "arpl",
                    "clts",
                    "lar", "lgdt", "lidt", "lldt", "lmsw", "loadall", "lsl", "ltr", "sgdt", "sidt", "sldt", "smsw",
                    "str",
                    "verr", "verw", "bsf", "bsr", "bt", "btc", "btr", "bts", "cdq", "cmpsd", "cwde", "insd", "iret",
                    "iretw",
                    "iretd", "jcxz", "jecxz", "lfs", "lgs", "lss", "lodsd", "movsd", "movsx", "movzx", "outsd", "popad",
                    "popfd", "pushad", "pushfd", "scasd", "seta", "setae", "setb", "setbe", "setc", "sete", "setg",
                    "setge",
                    "setl", "setle", "setna", "setnae", "setnb", "setnbe", "setnc", "setne", "setng", "setnge", "setnl",
                    "setnle", "setno", "setnp", "setns", "setnz", "seto", "setp", "setpe", "setpo", "sets", "setz",
                    "shld",
                    "shrd", "stosd", "popad", "popfd", "pushad", "pushfd", "scasd", "bswap", "cmpxchg", "invd",
                    "invlpg",
                    "wbinvd", "xadd", "cpuid", "cmpxchg8b", "rdmsr", "rdtsc", "wrmsr", "rsm", "rdpmc", "cmova",
                    "cmovae",
                    "cmovb", "cmovbe", "cmovc", "cmove", "cmovg", "cmovge", "cmovl", "cmovle", "cmovna", "cmovnae",
                    "cmovnb",
                    "cmovnbe", "cmovnc", "cmovne", "cmovng", "cmovnge", "cmovnl", "cmovnle", "cmovno", "cmovnp",
                    "cmovns",
                    "cmovnz", "cmovo", "cmovp", "cmovpe", "cmovpo", "cmovs", "cmovz", "f2xm1", "fabs", "fadd", "faddp",
                    "fbld",
                    "fbstp", "fchs", "fclex", "fcom", "fcomp", "fcompp", "fdecstp", "fdisi", "fdiv", "fdivp", "fdivr",
                    "fdivrp",
                    "feni", "ffree", "fiadd", "ficom", "ficomp", "fidiv", "fidivr", "fild", "fimul", "fincstp", "finit",
                    "fist",
                    "fistp", "fisub", "fisubr", "fld", "fld1", "fldcw", "fldenv", "fldenvw", "fldl2e", "fldl2t",
                    "fldlg2",
                    "fldln2", "fldpi", "fldz", "fmul", "fmulp", "fnclex", "fndisi", "fneni", "fninit", "fnop", "fnsave",
                    "fnsavew", "fnstcw", "fnstenv", "fnstenvw", "fnstsw", "fpatan", "fprem", "fptan", "frndint",
                    "frstor",
                    "frstorw", "fsave", "fsavew", "fscale", "fsqrt", "fst", "fstcw", "fstenv", "fstenvw", "fstp",
                    "fstsw",
                    "fsub", "fsubp", "fsubr", "fsubrp", "ftst", "fwait", "fxam", "fxch", "fxtract", "fyl2x", "fyl2xp1",
                    "fsetpm", "fcos", "fldenvd", "fsaved", "fstenvd", "fprem1", "frstord", "fsin", "fsincos", "fstenvd",
                    "fucom", "fucomp", "fucompp", "fcmovb", "fcmovbe", "fcmove", "fcmovnb", "fcmovnbe", "fcmovne",
                    "fcmovnu",
                    "fcmovu", "fcomi", "fcomip", "fucomi", "fucomip", "cdqe", "cqo", "movmskps", "movmskpd", "popcnt",
                    "lzcnt",
                    "cmpsq", "scasq", "movsq", "lodsq", "stosq", "jrcxz", "iretq", "pushfq", "popfq", "cmpxchg16b",
                    "jrcxz",
                    "insb", "insw", "outsb", "outsw", "lfence", "sfence", "mfence", "prefetch", "prefetchl",
                    "prefetchw",
                    "clflush", "sysenter", "sysexit", "syscall", "sysret"]
KEYWORD_REGEX = QRegularExpression(str.join("|", [f"\\b{keyword}\\b" for keyword in KEYWORD_PATTERNS]),
                                   QRegularExpression.CaseInsensitiveOption)

# noinspection SpellCheckingInspection
MEMORY_PATTERNS = ["\\bresb\\b", "\\bresw\\b", "\\bresd\\b", "\\bresq\\b", "\\brest\\b", "\\breso\\b", "\\bresy\\b",
                   "\\bddq\\b", "\\bresdq\\b", "\\bdb\\b", "\\bdw\\b", "\\bdd\\b", "\\bdq\\b", "\\bdt\\b", "\\bdo\\b",
                   "\\bdy\\b", "\\bequ\\b", "\\bbyte[\\s\\[]", "\\bword[\\s\\[]", "\\bdword[\\s\\[]",
                   "\\bqword[\\s\\[]", "\\btword[\\s\\[]", "\\boword[\\s\\[]", "\\byword[\\s\\[]", "\\[", "\\]"]
MEMORY_REGEX = QRegularExpression(str.join("|", MEMORY_PATTERNS), QRegularExpression.CaseInsensitiveOption)

# noinspection SpellCheckingInspection
REGISTER_PATTERNS = ["eax", "ebx", "ecx", "edx", "ebp", "esp", "edi", "esi", "ax", "bx", "cx", "dx", "bp", "sp", "si",
                     "di", "al", "ah", "bl", "bh", "cl", "ch", "dl", "dh",
                     # 64 bit registers
                     "rax", "rbx", "rcx", "rdx", "rbp", "rsp", "rdi", "rsi", "spl", "bpl", "sil", "dil", "r8", "r8d",
                     "r8w", "r8b", "r9", "r9d", "r9w", "r9b", "r10", "r10d", "r10w", "r10b", "r11", "r11d", "r11w",
                     "r11b", "r12", "r12d", "r12w", "r12b", "r13", "r13d", "r13w", "r13b", "r14", "r14d", "r14w",
                     "r14b", "r15", "r15d", "r15w", "r15b"]
REGISTER_REGEX = QRegularExpression(str.join("|", [f"\\b{register}\\b" for register in REGISTER_PATTERNS]),
                                    QRegularExpression.CaseInsensitiveOption)

LABEL_PATTERNS = ["\\.[^\\s:]+[^:]", "\\.[^\\s:]+:", "\\S+:"]
LABEL_REGEX = QRegularExpression(str.join("|", LABEL_PATTERNS))

NUMBER_PATTERNS = ["\\b[\\-\\+]?\\d+\\.\\d+\\b", "\\b0[bo]\\d+\\b", "\\b[0-9A-Fa-f]+h\\b", "\\b0[xh][0-9A-Fa-f]+\\b",
                   "\\b[\\-\\+]?\\d+[bod]?\\b"]
NUMBER_REGEX = QRegularExpression(str.join("|", NUMBER_PATTERNS))

# noinspection SpellCheckingInspection
SYSTEM_PATTERNS = ["\\btimes\\b", "\\bsection\\b", "\\.bss\\b", "\\.text\\b", "\\.data\\b", "\\bglobal\\b",
                   "\\.rodata\\b", "\\bextern\\b", "\\%arg\\b", "\\%assign\\b", "\\%clear\\b", "\\%comment\\b",
                   "\\%define\\b", "\\%defstr\\b", "\\%deftok\\b", "\\%depend\\b", "\\%line\\b", "\\%local\\b",
                   "\\%macro\\b", "\\%n\\b", "\\%pathsearch\\b", "\\%pop\\b", "\\%push\\b", "\\%rep\\b", "\\%repl\\b",
                   "\\%rotate\\b", "\\%stacksize\\b", "\\%strcat\\b", "\\%strlen\\b", "\\%substr\\b", "\\%undef\\b",
                   "\\%unmacro\\b", "\\%use\\b", "\\%warning\\b", "\\%xdefine\\b", "\\%endcomment\\b", "\\%endif\\b",
                   "\\%endmacro\\b", "\\%endrep\\b", "\\%error\\b", "\\%exitrep\\b", "\\%fatal\\b", "\\%idefine\\b",
                   "\\%else\\b", "\\%imacro\\b", "\\%include\\b", "\\%if\\b", "\\%ifctx\\b", "\\%ifdef\\b",
                   "\\%ifempty\\b", "\\%ifenv\\b", "\\%ifidn\\b", "\\%ifidni\\b", "\\%ifmacro\\b", "\\%ifstr\\b",
                   "\\%iftoken\\b", "\\%ifnum\\b", "\\%ifid\\b", "\\%elif\\b", "\\%elifctx\\b", "\\%elifdef\\b",
                   "\\%elifempty\\b", "\\%elifenv\\b", "\\%elifidn\\b", "\\%elifidni\\b", "\\%elifmacro\\b",
                   "\\%elifstr\\b", "\\%eliftoken\\b", "\\%elifnum\\b", "\\%elifid\\b", "\\%ifn\\b", "\\%ifnctx\\b",
                   "\\%ifndef\\b", "\\%ifnempty\\b", "\\%ifnenv\\b", "\\%ifnidn\\b", "\\%ifnidni\\b", "\\%ifnmacro\\b",
                   "\\%ifnstr\\b", "\\%ifntoken\\b", "\\%ifnnum\\b", "\\%ifnid\\b", "\\%elifn\\b", "\\%elifnctx\\b",
                   "\\%elifndef\\b", "\\%elifnempty\\b", "\\%elifnenv\\b", "\\%elifnidn\\b", "\\%elifnidni\\b",
                   "\\%elifnmacro\\b", "\\%elifnstr\\b", "\\%elifntoken\\b", "\\%elifnnum\\b", "\\%elifnid\\b"]
SYSTEM_REGEX = QRegularExpression(str.join("|", SYSTEM_PATTERNS), QRegularExpression.CaseInsensitiveOption)

QUOTES_PATTERNS = ["\"[^\"]*\"", "'[^']*'", "`[^`]*`"]
QUOTES_REGEX = QRegularExpression(str.join("|", QUOTES_PATTERNS))

SINGLE_LINE_COMMENT_PATTERNS = [";[^\n]*"]
SINGLE_LINE_COMMENT_REGEX = QRegularExpression(str.join("|", SINGLE_LINE_COMMENT_PATTERNS))


class NASMHighlighter(QSyntaxHighlighter):
    """ Highlight NASM syntax in files! """

    def __init__(self, document: QTextDocument):
        super().__init__(document)

        self.highlighting_rules = []

        keyword_format = QTextCharFormat()
        keyword_format.setForeground(Qt.blue)
        keyword_format.setFontWeight(QFont.Bold)

        memory_format = QTextCharFormat()
        memory_format.setForeground(QColor(0, 128, 255))

        register_format = QTextCharFormat()
        register_format.setForeground(QColor(153, 0, 204))

        label_format = QTextCharFormat()
        label_format.setForeground(QColor(128, 0, 0))

        number_format = QTextCharFormat()
        number_format.setForeground(QColor(255, 122, 0))

        system_format = QTextCharFormat()
        system_format.setForeground(Qt.darkCyan)

        quotes_format = QTextCharFormat()
        quotes_format.setForeground(QColor(128, 128, 128))

        comment_format = QTextCharFormat()
        comment_format.setForeground(Qt.darkGreen)

        # Note that the order these are applied in matters!
        self.highlighting_rules.append(HighlightingRule(pattern=KEYWORD_REGEX, format=keyword_format))
        self.highlighting_rules.append(HighlightingRule(pattern=MEMORY_REGEX, format=memory_format))
        self.highlighting_rules.append(HighlightingRule(pattern=REGISTER_REGEX, format=register_format))
        self.highlighting_rules.append(HighlightingRule(pattern=LABEL_REGEX, format=label_format))
        self.highlighting_rules.append(HighlightingRule(pattern=NUMBER_REGEX, format=number_format))
        self.highlighting_rules.append(HighlightingRule(pattern=SYSTEM_REGEX, format=system_format))
        self.highlighting_rules.append(HighlightingRule(pattern=QUOTES_REGEX, format=quotes_format))
        self.highlighting_rules.append(HighlightingRule(pattern=SINGLE_LINE_COMMENT_REGEX, format=comment_format))

    def highlightBlock(self, text: str):
        """
        Highlight the given text block, which is assumed to be one line of text. This is the case
        with a QPlainTextEdit widget.
        """
        for rule in self.highlighting_rules:
            match_iterator: QRegularExpressionMatchIterator = rule.pattern.globalMatch(text)
            while match_iterator.hasNext():
                match: QRegularExpressionMatch = match_iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), rule.format)
