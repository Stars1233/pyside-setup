// Copyright (C) 2017 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR GPL-3.0-only WITH Qt-GPL-exception-1.0

#ifndef COMPILERSUPPORT_H
#define COMPILERSUPPORT_H

#include <QtCore/qbytearraylist.h>

QT_FORWARD_DECLARE_CLASS(QVersionNumber)
QT_FORWARD_DECLARE_CLASS(QString)

enum class LanguageLevel {
    Default,
    Cpp11,
    Cpp14,
    Cpp17,
    Cpp20,
    Cpp1Z
};

enum class Compiler {
    Msvc,
    Gpp,
    Clang
};

enum class Platform {
    Unix,
    Linux,
    Windows,
    macOS,
    Android,
    iOS
};

enum class Architecture {
    Other,
    X64,
    X86,
    Arm64,
    Arm32
};

namespace clang {
QVersionNumber libClangVersion();

QByteArrayList emulatedCompilerOptions(LanguageLevel level);
LanguageLevel emulatedCompilerLanguageLevel();

const char *languageLevelOption(LanguageLevel l);
LanguageLevel languageLevelFromOption(const char *);

QByteArrayList detectVulkan();

Compiler compiler();
bool setCompiler(const QString &name);

QString compilerFromCMake();

const QString &compilerPath();
void setCompilerPath(const QString &name);
void addCompilerArgument(const QString &arg);

Platform platform();
bool setPlatform(const QString &name);

Architecture architecture();
bool setArchitecture(const QString &name);

unsigned pointerSize(); // (bit)
void setPointerSize(unsigned ps); // Set by parser

QString targetTriple();
void setTargetTriple(const QStringList &clangOptions); // Set from cmd line before parsing
void setTargetTriple(const QString &t); // Updated by clang parser while parsing

} // namespace clang

#endif // COMPILERSUPPORT_H
