// SPDX-FileCopyrightText: 2023 SAP SE
//
// SPDX-License-Identifier: Apache-2.0
//
// This file is part of FEDEM - https://openfedem.org
////////////////////////////////////////////////////////////////////////////////

/*!
  \file test_FFaContainers.C
  \brief Unit testing for the FFaContainers library.
  \details This file is to provide unit tests for the FFaContainers library.
  These tests are added here and not in the fedem-foundation repositry, since
  the local build of fedem-foundation does not include FFaContainers.
*/

#include "gtest.h"
#include "FFaLib/FFaContainers/FFaFieldContainer.H"
#include "FFaLib/FFaContainers/FFaReference.H"


class FmDummy : public FFaFieldContainer
{
public:
  FmDummy(int uid = 0)
  {
    FFA_FIELD_INIT(myID,uid,"ID");
    FFA_REFERENCE_FIELD_INIT(myParentField,myParent,"PARENT");
    myParent.setPrintIfZero(false);
  }

  FFaField<int>               myID;
  FFaReference<FmDummy>       myParent;
  FFaField<FFaReferenceBase*> myParentField;
};


/*!
  Creates some FFaField tests.
*/

TEST(TestFFa,FFaReference)
{
  FmDummy a(1), b(2), c(3), d(4);
  a.myParent = &d;
  b.myParent = &d;
  c.myParent = &b;

  EXPECT_TRUE(a.myParent == b.myParent);
  EXPECT_TRUE(a.myParent != c.myParent);
  EXPECT_TRUE(a.myParentField == "1");
  EXPECT_TRUE(a.myParentField != "3");
}
