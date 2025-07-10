// Copyright (C) 2017 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR GPL-3.0-only WITH Qt-GPL-exception-1.0

#ifndef COMPILERSUPPORT_H
#define COMPILERSUPPORT_H

#include <QtCore/qbytearraylist.h>
#include <QtCore/qversionnumber.h>

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
QByteArray targetTripletForPlatform(Platform p, Architecture a, Compiler c,
                                    const QVersionNumber &platformVersion = {});
const char *compilerTripletValue(Compiler c);

Architecture architecture();
bool setArchitecture(const QString &name);

unsigned pointerSize(); // (bit)
void setPointerSize(unsigned ps); // Set by parser

QString targetTriple();
void setTargetTriple(const QString &t); // Updated by clang parser while parsing

bool isCrossCompilation();

// Are there any options specifying a target
bool hasTargetOption(const QByteArrayList &clangOptions);

// Unless the platform/architecture/compiler options were set, try to find
// values based on a --target option in clangOptions and the compiler path.
void setHeuristicOptions(const QByteArrayList &clangOptions);

// Parse a triplet "x86_64-unknown-linux-gnu" (for testing). Note the
// compiler might not be present and defaults to host
bool parseTriplet(QStringView name, Architecture *a, Platform *p, Compiler *c,
                  QVersionNumber *version);

} // namespace clang

#endif // COMPILERSUPPORT_H
