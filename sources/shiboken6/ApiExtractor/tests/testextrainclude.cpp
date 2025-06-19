// Copyright (C) 2016 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR GPL-3.0-only WITH Qt-GPL-exception-1.0

#include "testextrainclude.h"
#include "testutil.h"

#include <abstractmetalang.h>
#include <complextypeentry.h>
#include <typesystemtypeentry.h>
#include <clangparser/compilersupport.h>

#include <QtTest/qtest.h>

using namespace Qt::StringLiterals;

void TestExtraInclude::testClassExtraInclude()
{
    const char cppCode[] = "struct A {};\n";
    const char xmlCode[] = "\
    <typesystem package='Foo'>\n\
        <value-type name='A'>\n\
            <extra-includes>\n\
                <include file-name='header.h' location='global'/>\n\
            </extra-includes>\n\
        </value-type>\n\
    </typesystem>\n";

    QScopedPointer<AbstractMetaBuilder> builder(TestUtil::parse(cppCode, xmlCode, false));
    QVERIFY(builder);
    AbstractMetaClassList classes = builder->classes();
    const auto classA = AbstractMetaClass::findClass(classes, "A");
    QVERIFY(classA);

    QList<Include> includes = classA->typeEntry()->extraIncludes();
    QCOMPARE(includes.size(), 1);
    QCOMPARE(includes.constFirst().name(), u"header.h");
}

void TestExtraInclude::testGlobalExtraIncludes()
{
    const char cppCode[] = "struct A {};\n";
    const char xmlCode[] = "\
    <typesystem package='Foo'>\n\
        <extra-includes>\n\
            <include file-name='header1.h' location='global'/>\n\
            <include file-name='header2.h' location='global'/>\n\
        </extra-includes>\n\
        <value-type name='A'/>\n\
    </typesystem>\n";

    QScopedPointer<AbstractMetaBuilder> builder(TestUtil::parse(cppCode, xmlCode, false));
    QVERIFY(builder);
    AbstractMetaClassList classes = builder->classes();
    QVERIFY(AbstractMetaClass::findClass(classes, "A"));

    auto *td = TypeDatabase::instance();
    TypeSystemTypeEntryCPtr module = td->defaultTypeSystemType();
    QVERIFY(module);
    QCOMPARE(module->name(), u"Foo");

    QList<Include> includes = module->extraIncludes();
    QCOMPARE(includes.size(), 2);
    QCOMPARE(includes.constFirst().name(), u"header1.h");
    QCOMPARE(includes.constLast().name(), u"header2.h");
}

void TestExtraInclude::testParseTriplet_data()
{
    QTest::addColumn<QString>("triplet");
    QTest::addColumn<bool>("expectedOk");
    QTest::addColumn<Architecture>("expectedArchitecture");
    QTest::addColumn<Platform>("expectedPlatform");
    QTest::addColumn<bool>("expectedCompilerPresent");
    QTest::addColumn<Compiler>("expectedCompiler");
    QTest::addColumn<QByteArray>("expectedConverted"); // test back-conversion

    QTest::newRow("Invalid")
        << QString("Invalid"_L1)
        << false << Architecture::X64 << Platform::Linux << false << Compiler::Gpp
        << QByteArray{};

    QTest::newRow("Linux")
        << QString("x86_64-unknown-linux-gnu"_L1)
        << true << Architecture::X64 << Platform::Linux << true << Compiler::Gpp
        << "x86_64-unknown-linux-gnu"_ba;

    QTest::newRow("WindowsArm")
        << QString("aarch64-pc-windows-msvc19.39.0"_L1)
        << true << Architecture::Arm64 << Platform::Windows << true << Compiler::Msvc
        << "arm64-pc-windows-msvc"_ba;

    QTest::newRow("Apple")
        << QString("arm64-apple-macosx15.0.0"_L1)
        << true << Architecture::Arm64 << Platform::macOS << false << Compiler::Gpp
        << "arm64-apple-macosx"_ba;

    QTest::newRow("AndroidArm32")
        << QString("armv7a-none-linux-android5.1"_L1)
        << true << Architecture::Arm32 << Platform::Android << false << Compiler::Gpp
        << "armv7a-unknown-linux-android"_ba;

    QTest::newRow("AndroidArm64")
        << QString("aarch64-none-linux-androideabi27.1"_L1)
        << true << Architecture::Arm64 << Platform::Android << false << Compiler::Gpp
        << "aarch64-unknown-linux-android"_ba;

    QTest::newRow("iOS")
        << QString("arm64-apple-ios"_L1)
        << true << Architecture::Arm64 << Platform::iOS << false << Compiler::Gpp
        << "arm64-apple-ios"_ba;
}

void TestExtraInclude::testParseTriplet()
{
    QFETCH(QString, triplet);
    QFETCH(bool, expectedOk);
    QFETCH(Architecture, expectedArchitecture);
    QFETCH(Platform, expectedPlatform);
    QFETCH(bool, expectedCompilerPresent);
    QFETCH(Compiler, expectedCompiler);
    QFETCH(QByteArray, expectedConverted);

    Architecture actualArchitecture{};
    Platform actualPlatform{};
    Compiler actualCompiler{};

    const bool ok = clang::parseTriplet(triplet, &actualArchitecture, &actualPlatform, &actualCompiler);
    QCOMPARE(ok, expectedOk);
    if (ok) {
        QCOMPARE(actualArchitecture, expectedArchitecture);
        QCOMPARE(actualPlatform, expectedPlatform);
        if (expectedCompilerPresent)
            QCOMPARE(expectedCompiler, actualCompiler);
        if (expectedOk) {
            auto actualConverted = clang::targetTripletForPlatform(actualPlatform, actualArchitecture, actualCompiler);
            QCOMPARE(actualConverted, expectedConverted);
        }
    }
}

QTEST_APPLESS_MAIN(TestExtraInclude)
